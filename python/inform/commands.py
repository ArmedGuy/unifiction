def set_param(device, action):
    if "mgmt_cfg" in action:
        params = action["mgmt_cfg"].split("\n")
        for p in params:
            key, _, val = p.partition("=")
            if key == "cfgversion":
                device.cfgversion = val
    if "cfgversion" in action:
        device.cfgversion = action["cfgversion"]
    
    if "system_cfg" in action:
        params = action["system_cfg"].split("\n")
        for p in params:
            key, _, val = p.partition("=")
                
    device.adopted = True

COMMAND_LIST = {
    "setparam": set_param
}