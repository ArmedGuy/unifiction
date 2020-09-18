from inform.push import inform, do_inform

def set_adopt(device, inform_url, key):
    device.adopt(key, inform_url)
    device.phases["inform"] = device.go_run(inform, device)

COMMAND_LIST = {
    "set-adopt": set_adopt
}
