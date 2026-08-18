"""Tests for the number platform."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.brink_ventilation.const import CONF_HOST, CONF_PORT, DOMAIN
from custom_components.brink_ventilation.lib.brink import Brink

USER_INPUT = {CONF_HOST: "192.168.1.50", CONF_PORT: 502}

BYPASS_TEMPERATURE_ENTITIES = [
    (
        "number.brink_hrv_modbus_bypass_temperature_from_dwelling",
        "get_bypass_temperature_from_dwelling",
        "set_bypass_temperature_from_dwelling",
        22.0,
        15.0,
        35.0,
    ),
    (
        "number.brink_hrv_modbus_bypass_temperature_from_outside",
        "get_bypass_temperature_from_outside",
        "set_bypass_temperature_from_outside",
        10.0,
        7.0,
        15.0,
    ),
    (
        "number.brink_hrv_modbus_bypass_temperature_hysteresis",
        "get_bypass_temperature_hysteresis",
        "set_bypass_temperature_hysteresis",
        2.0,
        0.0,
        5.0,
    ),
]


def _mock_brink() -> MagicMock:
    """A Brink instance whose data-fetch methods all resolve successfully."""
    brink = MagicMock(spec=Brink)
    for attr in dir(Brink):
        if attr.startswith("get_"):
            setattr(brink, attr, AsyncMock(return_value=0))
    return brink


@pytest.mark.parametrize(
    ("entity_id", "getter_name", "_setter_name", "value", "min_value", "max_value"),
    BYPASS_TEMPERATURE_ENTITIES,
)
async def test_bypass_temperature_number_reports_value_and_bounds(
    hass, entity_id, getter_name, _setter_name, value, min_value, max_value
):
    entry = MockConfigEntry(domain=DOMAIN, data=USER_INPUT)
    entry.add_to_hass(hass)

    brink = _mock_brink()
    setattr(brink, getter_name, AsyncMock(return_value=value))

    with patch(
        "custom_components.brink_ventilation.coordinator.Brink.initialize",
        new=AsyncMock(return_value=brink),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get(entity_id)
    assert state is not None
    assert float(state.state) == value
    assert state.attributes["min"] == min_value
    assert state.attributes["max"] == max_value
    assert state.attributes["step"] == 0.5
    assert state.attributes["unit_of_measurement"] == "°C"


@pytest.mark.parametrize(
    ("entity_id", "_getter_name", "setter_name", "value", "_min_value", "_max_value"),
    BYPASS_TEMPERATURE_ENTITIES,
)
async def test_bypass_temperature_number_writes_new_value(
    hass, entity_id, _getter_name, setter_name, value, _min_value, _max_value
):
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
        "number",
        "set_value",
        {"entity_id": entity_id, "value": value},
        blocking=True,
    )

    getattr(brink, setter_name).assert_awaited_once_with(value)
