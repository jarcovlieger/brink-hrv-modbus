from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity)

STATUS = {
    "No Communication": 2,
    "Idle": 3,
    "Running": 4,
    "Blocked": 5,
    "Error": 6
}

from ..entity import BrinkEntity

class SupplyFanStatusSensor(BrinkEntity, SensorEntity):
    """Supply Fan Status Sensor"""

    _attr_name = "Supply Fan Status"
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_should_poll = False  # do not call update()
   
    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_supply_fan_status"  
        
    @property
    def native_value(self):
        for name, position in STATUS.items():
            if position == self.coordinator.supply_fan_status:
                return name
        return "Unknown"
    
    @property
    def icon(self):
        if self.coordinator.supply_fan_status == 3:  # Idle
            return "mdi:fan-off"
        elif self.coordinator.supply_fan_status == 4:  # Running
            return "mdi:fan"
        else:
            return "mdi:fan-alert"