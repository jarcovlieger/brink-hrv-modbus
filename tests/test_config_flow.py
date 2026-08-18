"""Tests for the config flow."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType
from pymodbus.exceptions import ConnectionException
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.brink_ventilation.const import CONF_HOST, CONF_PORT, DOMAIN

USER_INPUT = {CONF_HOST: "192.168.1.50", CONF_PORT: 502}


async def test_user_flow_creates_entry_on_successful_connection(hass):
    with patch(
        "custom_components.brink_ventilation.config_flow.Brink.initialize",
        new=AsyncMock(return_value=MagicMock()),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == USER_INPUT


async def test_user_flow_shows_cannot_connect_on_connection_failure(hass):
    with patch(
        "custom_components.brink_ventilation.config_flow.Brink.initialize",
        new=AsyncMock(side_effect=ConnectionException("refused")),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_aborts_on_duplicate_host_without_connecting(hass):
    MockConfigEntry(domain=DOMAIN, data=USER_INPUT).add_to_hass(hass)

    with patch(
        "custom_components.brink_ventilation.config_flow.Brink.initialize",
        new=AsyncMock(),
    ) as mock_initialize:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    mock_initialize.assert_not_called()
