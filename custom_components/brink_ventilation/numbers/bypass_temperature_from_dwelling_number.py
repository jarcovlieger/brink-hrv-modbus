"""
Number entity for the bypass-open dwelling temperature threshold (Modbus register 6101).
"""
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import EntityCategory

from ..entity import BrinkEntity

class BypassTemperatureFromDwellingNumber(BrinkEntity, NumberEntity):
    """Number entity for the bypass-open dwelling temperature threshold (register 6101)."""

    _attr_has_entity_name = True
    _attr_name = "Bypass Temperature From Dwelling"
    _attr_icon = "mdi:home-thermometer"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 15.0
    _attr_native_max_value = 35.0
    _attr_native_step = 0.5
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_bypass_temperature_from_dwelling"

    @property
    def native_value(self):
        return self.coordinator.bypass_temperature_from_dwelling

    async def async_set_native_value(self, value: float) -> None:
        """Write the new dwelling temperature threshold to the unit."""
        await self.coordinator.set_bypass_temperature_from_dwelling(value)
