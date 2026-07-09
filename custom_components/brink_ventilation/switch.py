"""Platform for switch integration."""

from __future__ import annotations

from .const import DOMAIN
from .switches.standby_switch import BrinkStandbySwitch

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        BrinkStandbySwitch(coordinator, entry.entry_id),
        ])
