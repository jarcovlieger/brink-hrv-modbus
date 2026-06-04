from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE
) 

from ..entity import BrinkEntity

class SupplyHumiditySensor(BrinkEntity, SensorEntity):
    """Supply Humidity Sensor"""

    _attr_name = "Supply Humidity"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False  # do not call update()
   
    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_supply_humidity"  
        
    @property
    def native_value(self):
        return self.coordinator.supply_humidity