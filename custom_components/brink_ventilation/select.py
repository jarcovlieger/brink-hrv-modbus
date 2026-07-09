"""Platform for select integration."""

from __future__ import annotations

from .const import DOMAIN
from .selects.signal_output_select import BrinkSignalOutputSelect

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        BrinkSignalOutputSelect(coordinator, entry.entry_id),
        ])
