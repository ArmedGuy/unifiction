package device

import (
	"encoding/hex"
	"io/ioutil"
	"os"
	"path"
	"strings"
)

type Device struct {
	Name         string `json:"name"`
	MAC          string `json:"mac"`
	IP           string `json:"ip"`
	UniFiModel   string `json:"model"`
	FWVersion    string `json:"fw_version"`
	DeviceDriver string `json:"device_driver"`
	Ports        int    `json:"ports"`

	Adopted     bool
	Provisioned bool

	CfgVersion string
	MgmtCfg    map[string]string
	SystemCfg  map[string]string
}

func (dev *Device) Load(devicePath string) {
	dev.MgmtCfg = make(map[string]string)
	dev.SystemCfg = make(map[string]string)
	info, err := os.Stat(devicePath)
	if err != nil || !info.IsDir() {
		return
	}
	mgmtCfg := path.Join(devicePath, dev.Name, "mgmt_cfg")
	data, err := ioutil.ReadFile(mgmtCfg)
	if err != nil {
		return
	}
	dev.Adopted = true
	for _, line := range strings.Split(string(data), "\n") {
		parts := strings.Split(line, "=")
		dev.MgmtCfg[parts[0]] = parts[1]
	}

	systemCfg := path.Join(devicePath, dev.Name, "system_cfg")
	data, err = ioutil.ReadFile(systemCfg)
	if err != nil {
		return
	}
	dev.Provisioned = true
	for _, line := range strings.Split(string(data), "\n") {
		parts := strings.Split(line, "=")
		dev.SystemCfg[parts[0]] = parts[1]
	}
}

func (dev *Device) Dump() string {
	data, _ := ioutil.ReadFile("C:\\Users\\johan\\Projects\\ubnt-unifake\\inform-usc8.txt")
	return string(data)
}

func (dev *Device) BinaryDump() []byte {
	return []byte(dev.Dump())
}

func (dev *Device) Command(cmd string) {

}

func (dev *Device) BinaryMAC() []byte {
	ret, _ := hex.DecodeString(strings.ReplaceAll(dev.MAC, ":", ""))
	return ret
}

func (dev *Device) GetKey() string {
	if key, ok := dev.MgmtCfg["auth.key"]; ok {
		return key
	}
	return "ba86f2bbe107c7c57eb5f2690775c712"
}
