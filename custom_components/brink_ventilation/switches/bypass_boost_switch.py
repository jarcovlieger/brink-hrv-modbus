"""
Switch entity to turn Brink HRV bypass boost on/off via Modbus register 6104.
"""
from homeassistant.components.switch import SwitchEntity

from ..entity import BrinkEntity

class BrinkBypassBoostSwitch(BrinkEntity, SwitchEntity):
    """Switch that toggles bypass boost on (6104=1) or off (6104=0)."""

    _attr_has_entity_name = True
    _attr_name = "Bypass Boost"
    _attr_icon = "mdi:fan-plus"
    _attr_should_poll = False  # do not call update()

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_bypass_boost"

    @property
    def is_on(self):
        return self.coordinator.bypass_boost == 1

    async def async_turn_on(self, **kwargs):
        """Turn bypass boost on (register 6104 = 1)."""
        await self.coordinator.set_bypass_boost(1)

    async def async_turn_off(self, **kwargs):
        """Turn bypass boost off (register 6104 = 0)."""
        await self.coordinator.set_bypass_boost(0)
