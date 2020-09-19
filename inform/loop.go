package inform

import (
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/ArmedGuy/unifiction/config"
	"github.com/ArmedGuy/unifiction/device"
)

func inform(cfg *config.Config, device *device.Device) uint {
	data := Pack(device)
	resp, err := http.Post(cfg.InformUrl, "application/octet-stream", data)
	if err != nil {
		log.Printf("[ERROR] inform: http.Post returned error %v\n", err)
		return 10
	}
	if resp.StatusCode != 200 {
		log.Printf("[ERROR] inform: Returned non-200 status for inform, code: %v, device: %v\n", resp.StatusCode, device.Name)
		return 10
	}
	action := Unpack(device, resp.Body)
	if action.Type != "noop" {
		if action.Type == "setparam" {
			if len(action.MgmtCfg) > 0 {
				device.WriteFile("mgmt_cfg", action.MgmtCfg)
			}
			if len(action.SystemCfg) > 0 {
				device.WriteFile("system_cfg", action.SystemCfg)
			}
			device.Load()
			if key, ok := device.MgmtCfg["authkey"]; ok {
				device.WriteFile("authkey", key)
			}
		}
		return inform(cfg, device)
	}
	return action.Interval
}

func MainLoop(wg *sync.WaitGroup, cfg *config.Config, device *device.Device) {
	defer wg.Done()
	log.Printf("[INFO] inform: Setting up device %v\n", device.Name)
	device.Load()

	for {
		log.Printf("[DEBUG] inform: Sending inform for %v to %v\n", device.Name, cfg.InformUrl)
		interval := inform(cfg, device)
		time.Sleep(time.Duration(interval) * time.Second)
	}
}
