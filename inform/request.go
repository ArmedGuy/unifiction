package inform

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/binary"
	"encoding/hex"

	"github.com/ArmedGuy/unifiction/device"
)

func getCrypto(key string) (cipher.AEAD, error) {
	ckey, _ := hex.DecodeString(key)
	block, err := aes.NewCipher(ckey)
	if err != nil {
		return nil, err
	}

	return cipher.NewGCMWithNonceSize(block, 16)

}

func Pack(dev *device.Device) *bytes.Buffer {
	var b bytes.Buffer
	binary.Write(&b, binary.BigEndian, uint32(1414414933)) // Magic
	binary.Write(&b, binary.BigEndian, uint32(0))          // Protocol Version
	binary.Write(&b, binary.BigEndian, dev.BinaryMAC())    // Device MAC address
	binary.Write(&b, binary.BigEndian, uint16(0x1|0x8))    // AES-GCM encrypted
	iv := make([]byte, 16)
	rand.Read(iv)
	binary.Write(&b, binary.BigEndian, iv)        // init vector/nonce
	binary.Write(&b, binary.BigEndian, uint32(1)) // payload version

	payload := dev.BinaryDump()
	l := len(payload) + 16
	binary.Write(&b, binary.BigEndian, uint32(l)) // payload length + GCM tag length
	aad := b.Bytes()

	var b2 bytes.Buffer
	binary.Write(&b2, binary.BigEndian, aad)

	crypto, _ := getCrypto(dev.GetKey())
	ciphered := crypto.Seal(nil, iv, payload, aad)
	binary.Write(&b2, binary.BigEndian, ciphered)

	return &b2
}
