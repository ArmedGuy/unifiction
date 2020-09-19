package inform

import (
	"encoding/json"
	"time"

	"github.com/ArmedGuy/unifiction/device"
)

type InformAction struct {
	Type       string `json:"_type"`
	CfgVersion string `json:"cfgversion"`
	MgmtCfg    string `json:"mgmt_cfg"`
	SystemCfg  string `json:"system_cfg"`
	Interval   uint   `json:"interval"`
}

type InformResponse struct {
	Architecture       string            `json:"architecture"`
	BoardRev           int               `json:"board_rev"`
	Bootid             int               `json:"bootid"`
	BootromVersion     string            `json:"bootrom_version"`
	Cfgversion         string            `json:"cfgversion"`
	Default            bool              `json:"default"`
	DhcpServerTable    []DhcpServerTable `json:"dhcp_server_table"`
	DiscoveryResponse  bool              `json:"discovery_response"`
	Dualboot           bool              `json:"dualboot"`
	EverCrash          bool              `json:"ever_crash"`
	FwCaps             int               `json:"fw_caps"`
	GatewayIP          string            `json:"gateway_ip"`
	GatewayMac         string            `json:"gateway_mac"`
	GuestKicks         int               `json:"guest_kicks"`
	GuestToken         string            `json:"guest_token"`
	HasEth1            bool              `json:"has_eth1"`
	HasFan             bool              `json:"has_fan"`
	HasSpeaker         bool              `json:"has_speaker"`
	HasTemperature     bool              `json:"has_temperature"`
	HashID             string            `json:"hash_id"`
	Hostname           string            `json:"hostname"`
	HwCaps             int               `json:"hw_caps"`
	IfTable            []IfTable         `json:"if_table"`
	InformURL          string            `json:"inform_url"`
	Internet           bool              `json:"internet"`
	IP                 string            `json:"ip"`
	Isolated           bool              `json:"isolated"`
	KernelVersion      string            `json:"kernel_version"`
	Locating           bool              `json:"locating"`
	Mac                string            `json:"mac"`
	ManufacturerID     int               `json:"manufacturer_id"`
	Model              string            `json:"model"`
	ModelDisplay       string            `json:"model_display"`
	Netmask            string            `json:"netmask"`
	Overheating        bool              `json:"overheating"`
	PortTable          []PortTable       `json:"port_table"`
	PowerSource        string            `json:"power_source"`
	PowerSourceVoltage string            `json:"power_source_voltage"`
	RequiredVersion    string            `json:"required_version"`
	RootSwitch         string            `json:"root_switch"`
	Satisfaction       int               `json:"satisfaction"`
	SelfrunBeacon      bool              `json:"selfrun_beacon"`
	Serial             string            `json:"serial"`
	ServiceMac         string            `json:"service_mac"`
	SSHSessionTable    []interface{}     `json:"ssh_session_table"`
	State              int               `json:"state"`
	StpPriority        int               `json:"stp_priority"`
	StreamToken        string            `json:"stream_token"`
	SwitchCaps         SwitchCaps        `json:"switch_caps"`
	SysErrorCaps       int               `json:"sys_error_caps"`
	SysStats           SysStats          `json:"sys_stats"`
	SystemStats        SystemStats       `json:"system-stats"`
	Time               int64             `json:"time"`
	TimeMs             int               `json:"time_ms"`
	TmReady            bool              `json:"tm_ready"`
	TotalMaxPower      int               `json:"total_max_power"`
	Uplink             string            `json:"uplink"`
	Uptime             int               `json:"uptime"`
	Version            string            `json:"version"`
}
type DhcpServerTable struct {
	Blocked  bool   `json:"blocked"`
	IP       string `json:"ip"`
	LastSeen int    `json:"last_seen"`
	Mac      string `json:"mac"`
	PortIdx  int    `json:"port_idx"`
	Vlan     int    `json:"vlan"`
}
type IfTable struct {
	IP          string `json:"ip"`
	Mac         string `json:"mac"`
	Name        string `json:"name"`
	Netmask     string `json:"netmask"`
	NumPort     int    `json:"num_port"`
	RxBytes     int    `json:"rx_bytes"`
	RxDropped   int    `json:"rx_dropped"`
	RxErrors    int    `json:"rx_errors"`
	RxMulticast int    `json:"rx_multicast"`
	RxPackets   int    `json:"rx_packets"`
	TxBytes     int    `json:"tx_bytes"`
	TxDropped   int    `json:"tx_dropped"`
	TxErrors    int    `json:"tx_errors"`
	TxPackets   int    `json:"tx_packets"`
}
type MacTable struct {
	Age    int    `json:"age"`
	IP     string `json:"ip"`
	Mac    string `json:"mac"`
	Static bool   `json:"static"`
	Uptime int    `json:"uptime"`
	Vlan   int    `json:"vlan"`
}
type PortTable struct {
	Autoneg      bool          `json:"autoneg"`
	Dot1XMode    string        `json:"dot1x_mode"`
	Dot1XStatus  string        `json:"dot1x_status"`
	Enable       bool          `json:"enable"`
	FlowctrlRx   bool          `json:"flowctrl_rx"`
	FlowctrlTx   bool          `json:"flowctrl_tx"`
	FullDuplex   bool          `json:"full_duplex"`
	IsUplink     bool          `json:"is_uplink"`
	Jumbo        bool          `json:"jumbo"`
	LldpTable    []interface{} `json:"lldp_table"`
	MacTable     []MacTable    `json:"mac_table"`
	Media        string        `json:"media"`
	PoeCaps      int           `json:"poe_caps"`
	PortIdx      int           `json:"port_idx"`
	PortPoe      bool          `json:"port_poe"`
	RxBroadcast  int           `json:"rx_broadcast"`
	RxBytes      int64         `json:"rx_bytes"`
	RxDropped    int           `json:"rx_dropped"`
	RxErrors     int           `json:"rx_errors"`
	RxMulticast  int           `json:"rx_multicast"`
	RxPackets    int           `json:"rx_packets"`
	Satisfaction int           `json:"satisfaction"`
	Speed        int           `json:"speed"`
	SpeedCaps    int           `json:"speed_caps"`
	StpPathcost  int           `json:"stp_pathcost"`
	StpState     string        `json:"stp_state"`
	TxBroadcast  int           `json:"tx_broadcast"`
	TxBytes      int64         `json:"tx_bytes"`
	TxDropped    int           `json:"tx_dropped"`
	TxErrors     int           `json:"tx_errors"`
	TxMulticast  int           `json:"tx_multicast"`
	TxPackets    int           `json:"tx_packets"`
	Up           bool          `json:"up"`
	PoeEnable    bool          `json:"poe_enable,omitempty"`
	PoeMode      string        `json:"poe_mode,omitempty"`
	PoeVoltage   string        `json:"poe_voltage,omitempty"`
}
type SwitchCaps struct {
	FeatureCaps          int `json:"feature_caps"`
	MaxAggregateSessions int `json:"max_aggregate_sessions"`
	MaxL3Intf            int `json:"max_l3_intf"`
	MaxMirrorSessions    int `json:"max_mirror_sessions"`
	MaxReservedRoutes    int `json:"max_reserved_routes"`
	MaxStaticRoutes      int `json:"max_static_routes"`
}
type SysStats struct {
	Loadavg1  string `json:"loadavg_1"`
	Loadavg15 string `json:"loadavg_15"`
	Loadavg5  string `json:"loadavg_5"`
	MemBuffer int    `json:"mem_buffer"`
	MemTotal  int    `json:"mem_total"`
	MemUsed   int    `json:"mem_used"`
}
type SystemStats struct {
	CPU    string `json:"cpu"`
	Mem    string `json:"mem"`
	Uptime string `json:"uptime"`
}

func GetResponse(dev *device.Device) *InformResponse {
	resp := &InformResponse{
		Architecture:      "x86",
		BoardRev:          1,
		Bootid:            1,
		BootromVersion:    "1",
		Cfgversion:        dev.CfgVersion,
		Default:           !dev.Adopted,
		DiscoveryResponse: !dev.Adopted,
		Dualboot:          true,
		EverCrash:         false,
		FwCaps:            0,
		HasEth1:           false,
		HasFan:            false,
		HasSpeaker:        false,
		HasTemperature:    false,
		HashID:            "0000000000000000",
		Hostname:          "UBNT",
		HwCaps:            0,
		IfTable: []IfTable{IfTable{
			IP:      dev.IP,
			Mac:     dev.MAC,
			Name:    "eth0",
			Netmask: "255.255.255.0",
		}},
		InformURL:      dev.InformURL,
		Internet:       true,
		IP:             dev.IP,
		Isolated:       false,
		Locating:       false,
		Mac:            dev.MAC,
		ManufacturerID: 4,
		Model:          dev.UniFiModel,
		ModelDisplay:   "US-24",
		Netmask:        "255.255.255.0",
		Overheating:    false,
		// PortTable
		PowerSource:        "wall",
		PowerSourceVoltage: "48",
		RequiredVersion:    "3.9.40",
		Satisfaction:       100,
		SelfrunBeacon:      true,
		Serial:             "tjosanhejsan",
		ServiceMac:         dev.MAC,
		State:              2, // idk what do
		StpPriority:        32768,
		SwitchCaps:         SwitchCaps{},
		SysErrorCaps:       0,
		Time:               time.Now().Unix(),
		TimeMs:             0,
		TmReady:            true,
		TotalMaxPower:      0,
		Uplink:             "eth0",
		Uptime:             0,
		Version:            dev.FWVersion,
	}

	datadump := dev.Command("dump")
	_ = json.Unmarshal(datadump, resp)
	return resp
}
