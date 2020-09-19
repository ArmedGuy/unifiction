package device

import (
	"encoding/hex"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"path"
	"strings"
)

type Device struct {
	Name             string   `json:"name"`
	MAC              string   `json:"mac"`
	IP               string   `json:"ip"`
	UniFiModel       string   `json:"model"`
	FWVersion        string   `json:"fw_version"`
	DeviceDriver     string   `json:"device_driver"`
	DeviceDriverArgs []string `json:"device_driver_args"`
	DriverParams     []string `json:"driver_params"`

	InformURL  string
	DevicePath string

	Adopted     bool
	Provisioned bool

	CfgVersion string
	MgmtCfg    map[string]string
	SystemCfg  map[string]string
}

func (dev *Device) Load() {
	log.Printf("[DEBUG] device: Loading %v from device path %v\n", dev.Name, dev.DevicePath)
	dev.MgmtCfg = make(map[string]string)
	dev.SystemCfg = make(map[string]string)
	info, err := os.Stat(path.Join(dev.DevicePath, dev.Name))
	if err != nil || !info.IsDir() {
		log.Printf("[DEBUG] device: Device folder not found for %v\n", dev.Name)
		return
	}
	mgmtCfg := path.Join(dev.DevicePath, dev.Name, "mgmt_cfg")
	data, err := ioutil.ReadFile(mgmtCfg)
	if err != nil {
		return
	}
	dev.Adopted = true
	for _, line := range strings.Split(string(data), "\n") {
		parts := strings.Split(line, "=")
		if len(parts) != 2 {
			continue
		}
		dev.MgmtCfg[parts[0]] = parts[1]
	}

	authKey := path.Join(dev.DevicePath, dev.Name, "authkey")
	data, err = ioutil.ReadFile(authKey)
	if err == nil {
		dev.MgmtCfg["authkey"] = string(data)
	}

	systemCfg := path.Join(dev.DevicePath, dev.Name, "system_cfg")
	data, err = ioutil.ReadFile(systemCfg)
	if err != nil {
		return
	}
	dev.Provisioned = true
	for _, line := range strings.Split(string(data), "\n") {
		parts := strings.Split(line, "=")
		if len(parts) != 2 {
			continue
		}
		dev.SystemCfg[parts[0]] = parts[1]
	}
	dev.CfgVersion = dev.MgmtCfg["cfgversion"]
}

func (dev *Device) WriteFile(file, data string) {
	info, err := os.Stat(path.Join(dev.DevicePath, dev.Name))
	perm := os.FileMode(0700)
	if err != nil || !info.IsDir() {
		log.Printf("[DEBUG] device: Device folder not found for %v, creating it\n", dev.Name)
		os.MkdirAll(path.Join(dev.DevicePath, dev.Name), os.ModeDir|perm)
	}
	cfg := path.Join(dev.DevicePath, dev.Name, file)
	ioutil.WriteFile(cfg, []byte(data), perm)
}

func (dev *Device) Command(action string) []byte {
	args := append(dev.DeviceDriverArgs, action, path.Join(dev.DevicePath, dev.Name))
	cmd := exec.Command(dev.DeviceDriver, args...)
	out, err := cmd.CombinedOutput()
	if err != nil {
		log.Printf("[ERROR] device: Failed action %v for %v, reason %v\n", action, dev.Name, err)
	}
	return out
}

func (dev *Device) BinaryMAC() []byte {
	ret, _ := hex.DecodeString(strings.ReplaceAll(dev.MAC, ":", ""))
	return ret
}

func (dev *Device) GetKey() string {
	if key, ok := dev.MgmtCfg["authkey"]; ok {
		return key
	}
	return "ba86f2bbe107c7c57eb5f2690775c712"
}
