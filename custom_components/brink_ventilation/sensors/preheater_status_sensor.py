from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity)

STATUS = {
    0: "Initialize",
    1: "Inactive",
    2: "Active",
    3: "Test mode",
}

from ..entity import BrinkEntity

class PreheaterStatusSensor(BrinkEntity, SensorEntity):
    """Preheater Status Sensor (register 4060)"""

    _attr_name = "Preheater Status"
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_preheater_status"

    @property
    def native_value(self):
        return STATUS.get(self.coordinator.preheater_status, "Unknown")
