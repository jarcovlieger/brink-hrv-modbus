from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity)

STATUS = {
    0: "Standby",
    1: "Bootloader",
    2: "Non Blocking Error",
    3: "Blocking Error",
    4: "Manual",
    5: "Holiday",
    6: "Night Ventilation",
    7: "Party",
    8: "Bypass Boost",
    9: "Normal Boost",
    10: "Auto CO2",
    11: "Auto eBus",
    12: "Auto Modbus",
    13: "Auto LAN/WLAN Portal",
    14: "Auto LAN/WLAN Local",
}

from ..entity import BrinkEntity

class ActiveFunctionSensor(BrinkEntity, SensorEntity):
    """Active Function Sensor (register 4020)"""

    _attr_name = "Active Function"
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_active_function"

    @property
    def native_value(self):
        return STATUS.get(self.coordinator.active_function, "Unknown")
