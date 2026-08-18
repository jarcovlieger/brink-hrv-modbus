from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfVolumeFlowRate
)

from ..entity import BrinkEntity

class ExhaustFlowSensor(BrinkEntity, SensorEntity):
    """Exhaust Flow Sensor"""

    _attr_name = "Exhaust Flow"
    _attr_native_unit_of_measurement = UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR
    _attr_device_class = SensorDeviceClass.VOLUME_FLOW_RATE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_exhaust_flow"

    @property
    def native_value(self):
        return self.coordinator.exhaust_flow
