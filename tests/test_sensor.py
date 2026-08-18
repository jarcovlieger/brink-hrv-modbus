"""Tests for the sensor platform."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.components.sensor import ATTR_STATE_CLASS, SensorStateClass
from homeassistant.const import ATTR_DEVICE_CLASS, ATTR_UNIT_OF_MEASUREMENT
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.brink_ventilation.const import CONF_HOST, CONF_PORT, DOMAIN
from custom_components.brink_ventilation.lib.brink import Brink

USER_INPUT = {CONF_HOST: "192.168.1.50", CONF_PORT: 502}


def _mock_brink() -> MagicMock:
    """A Brink instance whose data-fetch methods all resolve successfully."""
    brink = MagicMock(spec=Brink)
    for attr in dir(Brink):
        if attr.startswith("get_"):
            setattr(brink, attr, AsyncMock(return_value=0))
    return brink


async def test_flow_sensors_report_coordinator_values(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()
    brink.get_supply_fan_flow_setpoint = AsyncMock(return_value=100)
    brink.get_supply_fan_flow = AsyncMock(return_value=95)
    brink.get_exhaust_fan_flow_setpoint = AsyncMock(return_value=90)
    brink.get_exhaust_fan_flow = AsyncMock(return_value=85)

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    expected = {
        "sensor.brink_hrv_modbus_supply_flow_setpoint": "100",
        "sensor.brink_hrv_modbus_supply_flow": "95",
        "sensor.brink_hrv_modbus_exhaust_flow_setpoint": "90",
        "sensor.brink_hrv_modbus_exhaust_flow": "85",
    }
    for entity_id, expected_state in expected.items():
        state = hass.states.get(entity_id)
        assert state is not None, f"{entity_id} was not set up"
        assert state.state == expected_state
        assert state.attributes[ATTR_UNIT_OF_MEASUREMENT] == "m³/h"
        assert state.attributes[ATTR_DEVICE_CLASS] == "volume_flow_rate"
        assert state.attributes[ATTR_STATE_CLASS] == SensorStateClass.MEASUREMENT
