"""Platform for switch integration."""

from __future__ import annotations

from .switches.standby_switch import BrinkStandbySwitch

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    async_add_entities([
        BrinkStandbySwitch(coordinator, entry.entry_id),
        ])
