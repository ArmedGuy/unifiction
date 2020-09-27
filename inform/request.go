package inform

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"io"
	"log"

	"github.com/ArmedGuy/unifiction/config"
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

func Pack(cfg *config.Config, dev *device.Device) *bytes.Buffer {
	var b bytes.Buffer
	binary.Write(&b, binary.BigEndian, uint32(1414414933)) // Magic
	binary.Write(&b, binary.BigEndian, uint32(0))          // Protocol Version
	binary.Write(&b, binary.BigEndian, dev.BinaryMAC())    // Device MAC address
	binary.Write(&b, binary.BigEndian, uint16(0x1|0x8))    // AES-GCM encrypted
	iv := make([]byte, 16)
	rand.Read(iv)
	binary.Write(&b, binary.BigEndian, iv)        // init vector/nonce
	binary.Write(&b, binary.BigEndian, uint32(1)) // payload version

	inform := GetResponse(cfg, dev)
	payload, _ := json.Marshal(&inform)

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

func Unpack(dev *device.Device, data io.Reader) *InformAction {
	var b bytes.Buffer // write all aad data to separate buffer
	var bufInt uint32
	binary.Read(data, binary.BigEndian, &bufInt) // magic
	binary.Write(&b, binary.BigEndian, &bufInt)
	binary.Read(data, binary.BigEndian, &bufInt) // protocolversion
	binary.Write(&b, binary.BigEndian, &bufInt)
	mac := make([]byte, 6)
	binary.Read(data, binary.BigEndian, &mac)
	binary.Write(&b, binary.BigEndian, &mac)
	var bufShort uint16
	binary.Read(data, binary.BigEndian, &bufShort) // flags
	binary.Write(&b, binary.BigEndian, &bufShort)
	iv := make([]byte, 16)
	binary.Read(data, binary.BigEndian, &iv) // init vector/nonce
	binary.Write(&b, binary.BigEndian, &iv)
	binary.Read(data, binary.BigEndian, &bufInt) // payload version
	binary.Write(&b, binary.BigEndian, &bufInt)
	binary.Read(data, binary.BigEndian, &bufInt) // payload length
	binary.Write(&b, binary.BigEndian, &bufInt)
	payload := make([]byte, bufInt)
	binary.Read(data, binary.BigEndian, &payload)

	aad := b.Bytes()
	crypto, _ := getCrypto(dev.GetKey())
	unciphered, _ := crypto.Open(nil, iv, payload, aad)
	log.Printf("[DEBUG] inform-unpack: %v\n", string(unciphered))
	var action InformAction
	_ = json.Unmarshal(unciphered, &action)

	return &action
}
