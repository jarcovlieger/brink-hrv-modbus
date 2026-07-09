from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE
)

from ..entity import BrinkEntity

class FrostHeaterPowerSensor(BrinkEntity, SensorEntity):
    """Frost Heater Power Sensor (register 4071)"""

    _attr_name = "Frost Heater Power"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:radiator"
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_frost_heater_power"

    @property
    def native_value(self):
        return self.coordinator.frost_heater_power
