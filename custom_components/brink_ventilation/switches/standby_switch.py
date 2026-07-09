"""
Switch entity to place the Brink HRV unit into standby via Modbus register 8003.
"""
from homeassistant.components.switch import SwitchEntity

from ..entity import BrinkEntity

STANDBY = 1
NORMAL = 2

class BrinkStandbySwitch(BrinkEntity, SwitchEntity):
    """Switch that toggles the unit between standby (8003=1) and normal (8003=2)."""

    _attr_has_entity_name = True
    _attr_name = "Standby"
    _attr_icon = "mdi:power-standby"
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_standby"

    @property
    def is_on(self):
        return self.coordinator.standby_mode == STANDBY

    async def async_turn_on(self, **kwargs):
        """Enter standby (register 8003 = 1)."""
        await self.coordinator.set_standby_mode(STANDBY)

    async def async_turn_off(self, **kwargs):
        """Return to normal mode (register 8003 = 2)."""
        await self.coordinator.set_standby_mode(NORMAL)
