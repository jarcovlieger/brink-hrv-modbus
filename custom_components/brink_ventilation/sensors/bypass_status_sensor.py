from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity)

STATUS = {
    0: "Initialize",
    1: "Open",
    2: "Close",
    3: "Open",
    4: "Closed",
}

from ..entity import BrinkEntity

class BypassStatusSensor(BrinkEntity, SensorEntity):
    """Bypass Status Sensor (register 4050)"""

    _attr_name = "Bypass Status"
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_bypass_status"

    @property
    def native_value(self):
        return STATUS.get(self.coordinator.bypass_status, "Unknown")
