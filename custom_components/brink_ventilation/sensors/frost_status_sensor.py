from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity)

STATUS = {
    0: "Not Initialized",
    1: "Power-Up Delay",
    2: "No Frost",
    3: "No-Frost Delay",
    4: "Frost Control Start Delay",
    5: "Wait For Icing",
    6: "Ice Detected Delay",
    7: "Heating",
    8: "Wait For Free Heater",
    9: "Fan Control Start Delay",
    10: "Fan Control Wait Delay",
    11: "Fan Control",
    12: "Fan Off Delay",
    13: "Fan Off",
    14: "Fan Restarting",
    15: "Error",
    16: "Test Mode",
}

from ..entity import BrinkEntity

class FrostStatusSensor(BrinkEntity, SensorEntity):
    """Frost Status Sensor (register 4070)"""

    _attr_name = "Frost Status"
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_frost_status"

    @property
    def native_value(self):
        return STATUS.get(self.coordinator.frost_status, "Unknown")
