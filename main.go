package main

import (
	"flag"
	"log"
	"os"
	"strings"
	"sync"

	"github.com/ArmedGuy/unifiction/config"
	"github.com/ArmedGuy/unifiction/inform"
)

func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func main() {
	pathPtr := flag.String("conf", "config.json", "path to config file")

	flag.Parse()

	config, err := config.ParseConfig(*pathPtr)
	if err != nil {
		log.Fatalf("Unable to read config: %v", err)
	}

	//for _, dev := range config.Devices {
	//	if !fileExists(dev.DeviceDriver) {
	//		log.Fatalf("Unable to initialize, could not find device driver %v", dev.DeviceDriver)
	//	}
	//}
	var wg sync.WaitGroup
	for _, dev := range config.Devices {
		dev.InformURL = config.InformUrl
		dev.DevicePath = config.DevicePath
		driverParams := strings.Join(dev.DriverParams, "\n")
		dev.WriteFile("driver_params", driverParams)
		log.Printf("[DEBUG] main: Starting loop for %v\n", dev.Name)
		wg.Add(1)
		go inform.MainLoop(&wg, config, dev)
	}
	wg.Wait()
}
