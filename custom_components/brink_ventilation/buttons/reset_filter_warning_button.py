"""
Button entity to reset filter status for the custom Home Assistant integration.
"""
from homeassistant.components.button import ButtonEntity

from ..entity import BrinkEntity

class ResetFilterWarningButton(BrinkEntity, ButtonEntity):
    """Reset Filter Warning Button"""

    _attr_has_entity_name = True
    _attr_name = "Reset Filter Warning"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_reset_filter_warning" 

    async def async_press(self) -> None:
        """Handle the button press to reset the filter warning."""
        await self.coordinator.reset_filter_warning()
        await self.coordinator.async_request_refresh()
