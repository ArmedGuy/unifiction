import json
import copy
import struct
import binascii
from Crypto.Cipher import AES
from io import BytesIO


class BinaryDataStream(object):
    """Directional binary data stream
    Reads and writes binary data from any stream-like object. This object is
    not bi-directional. Does no interpertation just unpacking and packing.
    """

    def __init__(self, data):
        self.data = data

    @classmethod
    def for_output(cls):
        return cls(BytesIO())

    def read_int(self):
        return struct.unpack(">i", self.data.read(4))[0]

    def read_short(self):
        return struct.unpack(">h", self.data.read(2))[0]

    def read_string(self, length):
        return self.data.read(length).decode('utf-8')
    
    def read_bytes(self, length):
        return self.data.read(length)

    def write_int(self, data):
        self.data.write(struct.pack(">i", data))

    def write_short(self, data):
        self.data.write(struct.pack(">h", data))

    def write_bytes(self, data):
        self.data.write(data)

    def write_string(self, data):
        self.data.write(data.encode('utf-8'))

    def get_output(self):
        return self.data.getvalue()


class Cryptor(object):
    """AES encryption strategy
    Handles AES crypto by wrapping pycrypto. Does padding and un-padding as
    well as key conversions when needed.
    """

    def __init__(self, key, iv, aad):
        self.iv = iv
        self.key = key
        self.aad = aad
        self.tag = None
        self.cipher = AES.new(binascii.unhexlify(key), AES.MODE_GCM, nonce=iv)

    def decrypt(self, payload, tag):
        self.cipher.update(self.aad)
        return self.cipher.decrypt_and_verify(payload, tag)

    def encrypt(self, payload):
        self.cipher.update(self.aad)
        return self.cipher.encrypt_and_digest(payload.encode('utf-8'))


class InformPacket(object):
    """Inform model object
    Holds basic, parsed, inform packet data. Does some interpertation for
    fields like flags. Can be passed to and from the serialiser. This class
    only fully supports version 1 of the inform data protocol. Version 0
    payload parsing is not supported.
    """

    ENCRYPTED_FLAG = 0x1
    COMPRESSED_FLAG = 0x2
    ENCRYPTED_GCM_FLAG = 0x8

    def __init__(self, use_key=None):
        self.magic_number = None
        self.version = None
        self.mac_addr = None
        self.flags = None
        self.iv = None
        self.data_version = None
        self.data_length = 0
        self.raw_payload = None
        self.tag = None
        self._used_key = use_key
        self._encrypted_payload = None

    def response_copy(self):
        """Copy object for use in response
        Generates a deep copy of the object and removes the payload so that it
        can be used to respond to the station that send this inform request.
        """
        new_obj = copy.deepcopy(self)
        new_obj.raw_payload = None
        return new_obj

    @staticmethod
    def _format_mac_addr(mac_bytes):
        return ":".join(["%0.2x" % i for i in mac_bytes])

    def _has_flag(self, flag):
        return self.flags & flag != 0

    @property
    def formatted_mac_addr(self):
        return self._format_mac_addr(self.mac_addr)

    @property
    def is_encrypted(self):
        return self._has_flag(self.ENCRYPTED_FLAG)

    @property
    def is_compressed(self):
        return self._has_flag(self.COMPRESSED_FLAG)

    @property
    def payload(self):
        if self.data_version == 1:
            return json.loads(self.raw_payload)
        else:
            return self.raw_payload

    @property
    def aad(self):
        output = BinaryDataStream.for_output()

        output.write_int(self.magic_number)
        output.write_int(self.version)
        output.write_bytes(self.mac_addr)
        output.write_short(self.flags)
        output.write_bytes(self.iv)
        output.write_int(self.data_version)
        output.write_int(self.data_length)

        return output.get_output()

    @payload.setter
    def payload(self, value):
        self.raw_payload = json.dumps(value)


class InformSerializer(object):
    """Inform protocol version 1 parser/serializer
    Handles the parsing of the inform binary protocol to python objects and
    seralization of python objects to inform binary protocol. Handles
    cryptography and data formats. Compatible only with version 1 of the data
    format.
    """

    MASTER_KEY = "ba86f2bbe107c7c57eb5f2690775c712"
    PROTOCOL_MAGIC = 1414414933
    MAX_VERSION = 1

    def __init__(self, key=None, key_bag=None):
        self.key = key
        self.key_bag = key_bag or {}

    def _decrypt_payload(self, packet):
        i = 0
        key = self.key_bag.get(packet.formatted_mac_addr)

        for key in (key, self.key, self.MASTER_KEY):
            if key is None:
                continue

            decrypted = Cryptor(key, packet.iv, packet.aad).decrypt(packet.raw_payload, packet.tag)

            json.loads(decrypted.decode("utf-8"))
            packet.raw_payload = decrypted
            packet._used_key = key
            break

    def parse(self, input):
        input_stream = BinaryDataStream(BytesIO(input))

        packet = InformPacket()

        packet.magic_number = input_stream.read_int()
        assert packet.magic_number == self.PROTOCOL_MAGIC

        packet.version = input_stream.read_int()
        assert packet.version < self.MAX_VERSION

        packet.mac_addr = input_stream.read_bytes(6)
        packet.flags = input_stream.read_short()
        packet.iv = input_stream.read_bytes(16)
        packet.data_version = input_stream.read_int()
        packet.data_length = input_stream.read_int()

        packet.raw_payload = input_stream.read_bytes(packet.data_length - 16)
        packet.tag = input_stream.read_bytes(16)

        if packet.is_encrypted:
            self._decrypt_payload(packet)

        return packet

    def encrypt_payload(self, packet):
        if packet.data_version != 1:
            raise ValueError("Can no encrypt contents of pre 1.0 packets")
        if not packet._encrypted_payload:
            key = packet._used_key if packet._used_key else self.MASTER_KEY
            packet._encrypted_payload, packet.tag = Cryptor(key, packet.iv, packet.aad).encrypt(json.dumps(packet.payload))
        return packet._encrypted_payload

    def serialize(self, packet):
        output = BinaryDataStream.for_output()

        output.write_int(packet.magic_number)
        output.write_int(packet.version)
        output.write_bytes(packet.mac_addr)
        output.write_short(packet.flags)
        output.write_bytes(packet.iv)
        output.write_int(packet.data_version)
        output.write_int(packet.data_length)
        output.write_bytes(self.encrypt_payload(packet))
        output.write_bytes(packet.tag)

        return output.get_output()