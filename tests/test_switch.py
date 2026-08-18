"""Tests for the switch platform."""

from unittest.mock import AsyncMock, MagicMock, patch

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


async def test_bypass_boost_switch_reports_on_state(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()
    brink.get_bypass_boost = AsyncMock(return_value=1)

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("switch.brink_hrv_modbus_bypass_boost")
    assert state is not None
    assert state.state == "on"


async def test_bypass_boost_switch_turn_on_writes_register(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    await hass.services.async_call(
        "switch",
        "turn_on",
        {"entity_id": "switch.brink_hrv_modbus_bypass_boost"},
        blocking=True,
    )

    brink.set_bypass_boost.assert_awaited_once_with(1)


async def test_bypass_boost_switch_turn_off_writes_register(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    await hass.services.async_call(
        "switch",
        "turn_off",
        {"entity_id": "switch.brink_hrv_modbus_bypass_boost"},
        blocking=True,
    )

    brink.set_bypass_boost.assert_awaited_once_with(0)
