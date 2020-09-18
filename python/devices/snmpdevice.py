from . import GenericDevice
class Device(GenericDevice):
    def __init__(self, config, device_config):
        super().__init__(config, device_config)