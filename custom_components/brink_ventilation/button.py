"""Platform for button integration."""

from __future__ import annotations

from .const import DOMAIN
from .buttons.reset_filter_warning_button import ResetFilterWarningButton

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ResetFilterWarningButton(coordinator, entry.entry_id),
        ])
