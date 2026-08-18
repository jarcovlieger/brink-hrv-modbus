"""Tests for integration setup."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.config_entries import ConfigEntryState
from pymodbus.exceptions import ConnectionException, ModbusException
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


async def test_setup_entry_succeeds_when_device_is_reachable(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=_mock_brink()),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    # One entity per platform, to guard against a platform silently failing
    # to find the coordinator (e.g. during the runtime_data migration).
    for entity_id in (
        "sensor.brink_hrv_modbus_supply_temperature",
        "fan.brink_hrv_modbus_ventilation",
        "binary_sensor.brink_hrv_modbus_filter_status",
        "button.brink_hrv_modbus_reset_filter_warning",
        "number.brink_hrv_modbus_days_before_filter_warning",
        "switch.brink_hrv_modbus_standby",
        "select.brink_hrv_modbus_signal_output",
    ):
        state = hass.states.get(entity_id)
        assert state is not None, f"{entity_id} was not set up"
        assert state.state != "unavailable"


async def test_setup_entry_retries_when_initial_connection_fails(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(side_effect=ConnectionException("refused")),
    ):
        assert not await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_entry_retries_when_first_refresh_fails(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()
    brink.get_supply_fan_status = AsyncMock(side_effect=ModbusException("read failed"))

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert not await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
