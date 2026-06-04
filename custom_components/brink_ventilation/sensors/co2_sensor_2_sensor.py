from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION
) 

from ..entity import BrinkEntity

class CO2Sensor2Sensor(BrinkEntity, SensorEntity):
    """CO2 Sensor 2 Sensor"""

    _attr_name = "CO2 Sensor 2"
    _attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
    _attr_device_class = SensorDeviceClass.CO2
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False  # do not call update()
    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_co2_sensor_2"  
        
    @property
    def native_value(self):
        return self.coordinator.CO2_sensor_2