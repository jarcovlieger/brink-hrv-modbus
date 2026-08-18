"""
Select entity to override the Brink HRV bypass mode (Modbus register 6100).
"""
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory

from ..entity import BrinkEntity

OPTIONS = {
    "Automatic": 0,
    "Closed": 1,
    "Open": 2,
}

class BrinkBypassModeSelect(BrinkEntity, SelectEntity):
    """Select entity for the bypass mode override (register 6100)."""

    _attr_has_entity_name = True
    _attr_name = "Bypass Mode"
    _attr_icon = "mdi:valve"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_should_poll = False  # do not call update()
    _attr_options = list(OPTIONS.keys())

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_bypass_mode"

    @property
    def current_option(self):
        value = self.coordinator.bypass_mode
        for name, option_value in OPTIONS.items():
            if option_value == value:
                return name
        return None

    async def async_select_option(self, option: str) -> None:
        """Write the selected bypass mode to the unit."""
        await self.coordinator.set_bypass_mode(OPTIONS[option])
