"""Platform for sensor integration."""

from __future__ import annotations

import logging

from .sensors.supply_fan_status_sensor import SupplyFanStatusSensor
from .sensors.supply_temperature_sensor import SupplyTemperatureSensor
from .sensors.supply_humidity_sensor import SupplyHumiditySensor
from .sensors.exhaust_fan_status_sensor import ExhaustFanStatusSensor
from .sensors.exhaust_temperature_sensor import ExhaustTemperatureSensor 
from .sensors.exhaust_humidity_sensor import ExhaustHumiditySensor
from .sensors.bypass_status_sensor import BypassStatusSensor
from .sensors.preheater_status_sensor import PreheaterStatusSensor
from .sensors.preheater_capacity_sensor import PreheaterCapacitySensor
from .sensors.frost_status_sensor import FrostStatusSensor
from .sensors.operating_hours_sensor import OperatingHoursSensor
from .sensors.filter_used_in_hours_sensor import FilterUsedInHoursSensor
from .sensors.filter_used_in_cubic_meters_per_hour_sensor import FilterUsedInCubicMetersPerHourSensor
from .sensors.co2_sensor_1_status_sensor import CO2Sensor1StatusSensor
from .sensors.co2_sensor_2_status_sensor import CO2Sensor2StatusSensor
from .sensors.co2_sensor_3_status_sensor import CO2Sensor3StatusSensor
from .sensors.co2_sensor_4_status_sensor import CO2Sensor4StatusSensor
from .sensors.co2_sensor_1_sensor import CO2Sensor1Sensor
from .sensors.co2_sensor_2_sensor import CO2Sensor2Sensor
from .sensors.co2_sensor_3_sensor import CO2Sensor3Sensor
from .sensors.co2_sensor_4_sensor import CO2Sensor4Sensor
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SupplyFanStatusSensor(coordinator, entry.entry_id),
        SupplyTemperatureSensor(coordinator, entry.entry_id),
        SupplyHumiditySensor(coordinator, entry.entry_id),
        ExhaustTemperatureSensor(coordinator, entry.entry_id),
        ExhaustHumiditySensor(coordinator, entry.entry_id),
        ExhaustFanStatusSensor(coordinator, entry.entry_id),
        BypassStatusSensor(coordinator, entry.entry_id),
        PreheaterStatusSensor(coordinator, entry.entry_id),
        PreheaterCapacitySensor(coordinator, entry.entry_id),
        FrostStatusSensor(coordinator, entry.entry_id),
        OperatingHoursSensor(coordinator, entry.entry_id),
        FilterUsedInHoursSensor(coordinator, entry.entry_id),
        FilterUsedInCubicMetersPerHourSensor(coordinator, entry.entry_id),
        CO2Sensor1StatusSensor(coordinator, entry.entry_id),
        CO2Sensor2StatusSensor(coordinator, entry.entry_id),
        CO2Sensor3StatusSensor(coordinator, entry.entry_id),
        CO2Sensor4StatusSensor(coordinator, entry.entry_id),
        CO2Sensor1Sensor(coordinator, entry.entry_id),
        CO2Sensor2Sensor(coordinator, entry.entry_id),
        CO2Sensor3Sensor(coordinator, entry.entry_id),
        CO2Sensor4Sensor(coordinator, entry.entry_id),
        ])

