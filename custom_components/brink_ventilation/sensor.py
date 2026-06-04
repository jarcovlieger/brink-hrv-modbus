"""Platform for sensor integration."""

from __future__ import annotations

import logging

from custom_components.brink_ventilation.sensors.filter_used_in_hours_sensor import FilterUsedInHoursSensor
from .sensors.supply_temperature_sensor import SupplyTemperatureSensor
from .sensors.exhaust_temperature_sensor import ExhaustTemperatureSensor 
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SupplyTemperatureSensor(coordinator, entry.entry_id),
        ExhaustTemperatureSensor(coordinator, entry.entry_id),
        FilterUsedInHoursSensor(coordinator, entry.entry_id)
        ])

