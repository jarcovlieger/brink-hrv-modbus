from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTime
) 

from ..entity import BrinkEntity

class FilterUsedInHoursSensor(BrinkEntity, SensorEntity):
    """Filter Used in Hours Sensor"""

    _attr_name = "Filter Used in Hours"
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_should_poll = False  # do not call update()
   
    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_filter_used_in_hours"  
        
    @property
    def native_value(self):
        return self.coordinator.filter_used_in_hours