"""
Number entity for the bypass-open outside temperature threshold (Modbus register 6102).
"""
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import EntityCategory

from ..entity import BrinkEntity

class BypassTemperatureFromOutsideNumber(BrinkEntity, NumberEntity):
    """Number entity for the bypass-open outside temperature threshold (register 6102)."""

    _attr_has_entity_name = True
    _attr_name = "Bypass Temperature From Outside"
    _attr_icon = "mdi:thermometer"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 7.0
    _attr_native_max_value = 15.0
    _attr_native_step = 0.5
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_bypass_temperature_from_outside"

    @property
    def native_value(self):
        return self.coordinator.bypass_temperature_from_outside

    async def async_set_native_value(self, value: float) -> None:
        """Write the new outside temperature threshold to the unit."""
        await self.coordinator.set_bypass_temperature_from_outside(value)
