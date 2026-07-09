"""
Number entity to set the days before a filter warning for the custom Home Assistant integration.
"""
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfTime
from homeassistant.helpers.entity import EntityCategory

from ..entity import BrinkEntity

class FilterWarningDaysNumber(BrinkEntity, NumberEntity):
    """Number entity for the days before a filter warning (register 6120)."""

    _attr_has_entity_name = True
    _attr_name = "Days Before Filter Warning"
    _attr_icon = "mdi:air-filter"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_native_unit_of_measurement = UnitOfTime.DAYS
    _attr_native_min_value = 1
    _attr_native_max_value = 365
    _attr_native_step = 1
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_filter_warning_days"

    @property
    def native_value(self):
        return self.coordinator.filter_warning_days

    async def async_set_native_value(self, value: float) -> None:
        """Write the new number of days before a filter warning to the unit."""
        await self.coordinator.set_filter_warning_days(int(value))
