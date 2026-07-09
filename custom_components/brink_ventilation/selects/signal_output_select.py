"""
Select entity to configure the Brink HRV signal output (Modbus register 6170).
"""
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory

from ..entity import BrinkEntity

OPTIONS = {
    "Off": 0,
    "Filter Warning": 1,
    "Error Status": 2,
    "Filter Warning and Error Status": 3,
}

class BrinkSignalOutputSelect(BrinkEntity, SelectEntity):
    """Select entity for the signal output setting (register 6170)."""

    _attr_has_entity_name = True
    _attr_name = "Signal Output"
    _attr_icon = "mdi:export"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_should_poll = False  # do not call update()
    _attr_options = list(OPTIONS.keys())

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_signal_output"

    @property
    def current_option(self):
        value = self.coordinator.signal_output
        for name, option_value in OPTIONS.items():
            if option_value == value:
                return name
        return None

    async def async_select_option(self, option: str) -> None:
        """Write the selected signal output option to the unit."""
        await self.coordinator.set_signal_output(OPTIONS[option])
