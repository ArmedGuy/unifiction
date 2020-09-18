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
	return 10
}

func MainLoop(wg *sync.WaitGroup, cfg *config.Config, device *device.Device) {
	defer wg.Done()
	log.Printf("[INFO] inform: Setting up device %v\n", device.Name)
	device.Load(cfg.DevicePath)

	for {
		log.Printf("[DEBUG] inform: Sending inform for %v to %v\n", device.Name, cfg.InformUrl)
		interval := inform(cfg, device)
		time.Sleep(time.Duration(interval) * time.Second)
	}
}
