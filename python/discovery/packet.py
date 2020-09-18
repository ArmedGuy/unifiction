import string

"""
packet raw len 148
packet payload len 144
field type: 0x2
field length 10
field data: b'\xe0c\xda\x8at\x90\xc0\xa8\x01\xf3'
---
field type: 0x1
field length 6
field data: b'\xe0c\xda\x8at\x90'
---
field type: 0xa
field length 4
field data: b'\x00\x00\x08\xf8'
---
field type: 0xb
field length 4
field data: b'UBNT'
---
field type: 0xc
field length 4
field data: b'USC8'
---
field type: 0x3
field length 36
field data: b'US.mscc7514.v3.9.54.9373.180913.2351'
---
field type: 0x16
field length 11
field data: b'3.9.54.9373'
---
field type: 0x15
field length 4
field data: b'USC8'
---
field type: 0x17
field length 1
field data: b'\x01'
---
field type: 0x18
field length 1
field data: b'\x00'
---
field type: 0x19
field length 1
field data: b'\x01'
---
field type: 0x1a
field length 1
field data: b'\x01'
---
field type: 0x13
field length 6
field data: b'\xe0c\xda\x8at\x90'
---
field type: 0x12
field length 4
field data: b'\x00\x00\x01\xb5'
---
field type: 0x1b
field length 6
field data: b'3.9.40'
---
"""

def i16(raw):
    return (int(raw[0]) << 8) + int(raw[1])

def decode(packet):
    print("packet raw len", len(packet))
    magic = packet[0:2]
    packet_size = i16(packet[2:4])
    print("packet payload len", packet_size)
    field_offset = 4
    ret = {}
    while packet_size > 0:
        field_type = int(packet[field_offset])
        field_len = i16(packet[field_offset+1:field_offset+3])
        data_end = field_offset+3+field_len
        print("field type: 0x%x" % field_type)
        print("field length", field_len)
        print("field data:", packet[field_offset+3:data_end])
        print("---")
        field_offset = data_end
        packet_size = packet_size - 3 - field_len

def build_packet(*args):
    p = {}
    out = b"\x02\x06" # magic header
    payload = bytes()
    for a in args:
        p.update(a)
    for t, data in p.items():
        payload += t
        dlen = len(data)
        payload += dlen.to_bytes(2, byteorder="big")
        payload += data
    plen = len(payload)
    return out + plen.to_bytes(2, byteorder='big') + payload

def ip_mac(ip, mac):
    rawmac = bytes()
    rawip = bytes()
    for p in mac.split(":"):
        rawmac += bytes.fromhex(p)
    for p in ip.split("."):
        rawip += int(p).to_bytes(1, byteorder='big')

    return {
        b'\x02': rawmac + rawip,
        b'\x01': rawmac,
        b'\x13': rawmac,
    }

def uptime(seconds):
    return {
        b'\x0a': seconds.to_bytes(4, byteorder='big')
    }

def model(model):
    return {
        b'\x0c': model.encode('utf-8'),
        b'\x15': model.encode('utf-8')
    }