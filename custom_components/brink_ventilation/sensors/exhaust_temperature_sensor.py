from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature
) 

from ..entity import BrinkEntity

class ExhaustTemperatureSensor(BrinkEntity, SensorEntity):
    """Exhaust Temperature Sensor"""

    _attr_name = "Exhaust Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False  # do not call update()
   
    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_exhaust_temperature"  
        
    @property
    def native_value(self):
        return self.coordinator.exhaust_temperature