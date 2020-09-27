package config

import (
	"encoding/json"
	"io/ioutil"

	"github.com/ArmedGuy/unifiction/device"
)

type Config struct {
	DevicePath string           `json:"device_path"`
	InformUrl  string           `json:"inform_url"`
	RootSwitch string           `json:"root_switch"`
	GatewayIP  string           `json:"gateway_ip"`
	GatewayMAC string           `json:"gateway_mac"`
	Devices    []*device.Device `json:"devices"`
}

func ParseConfig(path string) (*Config, error) {
	file, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	data := Config{}

	err = json.Unmarshal([]byte(file), &data)
	if err != nil {
		return nil, err
	}
	return &data, nil
}
