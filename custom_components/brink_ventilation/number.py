"""Platform for number integration."""

from __future__ import annotations

from .numbers.filter_warning_days_number import FilterWarningDaysNumber
from .numbers.bypass_temperature_from_dwelling_number import BypassTemperatureFromDwellingNumber
from .numbers.bypass_temperature_from_outside_number import BypassTemperatureFromOutsideNumber
from .numbers.bypass_temperature_hysteresis_number import BypassTemperatureHysteresisNumber

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    async_add_entities([
        FilterWarningDaysNumber(coordinator, entry.entry_id),
        BypassTemperatureFromDwellingNumber(coordinator, entry.entry_id),
        BypassTemperatureFromOutsideNumber(coordinator, entry.entry_id),
        BypassTemperatureHysteresisNumber(coordinator, entry.entry_id),
        ])
