"""Tests for the select platform."""

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


async def test_bypass_mode_select_reports_current_option(hass):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()
    brink.get_bypass_mode = AsyncMock(return_value=2)

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("select.brink_hrv_modbus_bypass_mode")
    assert state is not None
    assert state.state == "Open"
    assert state.attributes["options"] == ["Automatic", "Closed", "Open"]


async def test_bypass_mode_select_writes_chosen_option(hass):
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
        "select",
        "select_option",
        {"entity_id": "select.brink_hrv_modbus_bypass_mode", "option": "Closed"},
        blocking=True,
    )

    brink.set_bypass_mode.assert_awaited_once_with(1)
