from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity)

STATUS = {
    "Error": 0,
    "Not Initialized": 1,
    "Idle": 2,
    "Warming Up": 3,
    "Running": 4,
    "Calibrating": 5,
    "Self Test": 6
}

from ..entity import BrinkEntity

class CO2Sensor3StatusSensor(BrinkEntity, SensorEntity):
    """CO2 Sensor 3 Status Sensor"""

    _attr_name = "CO2 Sensor 3 Status"
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_should_poll = False  # do not call update()
    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_co2_sensor_3_status"  
        
    @property
    def native_value(self):
        for name, position in STATUS.items():
            if position == self.coordinator.CO2_sensor_3_status:
                return name
        return "Unknown"