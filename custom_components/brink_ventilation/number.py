"""Platform for number integration."""

from __future__ import annotations

from .const import DOMAIN
from .numbers.filter_warning_days_number import FilterWarningDaysNumber

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        FilterWarningDaysNumber(coordinator, entry.entry_id),
        ])
