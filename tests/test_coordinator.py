"""Unit tests for the Brink HRV Modbus coordinator."""

from unittest.mock import AsyncMock, MagicMock

from custom_components.brink_ventilation.coordinator import BrinkHrvModbusCoordinator
from custom_components.brink_ventilation.lib.brink import Brink


def _mock_brink() -> MagicMock:
    """A Brink instance whose data-fetch methods all resolve successfully."""
    brink = MagicMock(spec=Brink)
    for attr in dir(Brink):
        if attr.startswith("get_"):
            setattr(brink, attr, AsyncMock(return_value=0))
    return brink


async def test_update_data_populates_flow_attributes(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    brink.get_supply_fan_flow_setpoint = AsyncMock(return_value=100)
    brink.get_supply_fan_flow = AsyncMock(return_value=95)
    brink.get_exhaust_fan_flow_setpoint = AsyncMock(return_value=90)
    brink.get_exhaust_fan_flow = AsyncMock(return_value=85)
    coordinator._brink = brink

    await coordinator._async_update_data()

    assert coordinator.supply_flow_setpoint == 100
    assert coordinator.supply_flow == 95
    assert coordinator.exhaust_flow_setpoint == 90
    assert coordinator.exhaust_flow == 85


async def test_update_data_populates_active_function(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    brink.get_active_function = AsyncMock(return_value=8)
    brink.get_bypass_mode = AsyncMock(return_value=2)
    brink.get_bypass_temperature_from_dwelling = AsyncMock(return_value=22.0)
    brink.get_bypass_temperature_from_outside = AsyncMock(return_value=10.0)
    brink.get_bypass_temperature_hysteresis = AsyncMock(return_value=2.0)
    brink.get_bypass_boost = AsyncMock(return_value=1)
    coordinator._brink = brink

    await coordinator._async_update_data()

    assert coordinator.active_function == 8
    assert coordinator.bypass_mode == 2
    assert coordinator.bypass_temperature_from_dwelling == 22.0
    assert coordinator.bypass_temperature_from_outside == 10.0
    assert coordinator.bypass_temperature_hysteresis == 2.0
    assert coordinator.bypass_boost == 1


async def test_set_bypass_mode_writes_through_and_updates_state(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    coordinator._brink = brink

    await coordinator.set_bypass_mode(1)

    brink.set_bypass_mode.assert_awaited_once_with(1)
    assert coordinator.bypass_mode == 1


async def test_set_bypass_temperature_from_dwelling_writes_through_and_refreshes(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    brink.get_bypass_temperature_from_dwelling = AsyncMock(return_value=23.5)
    coordinator._brink = brink

    await coordinator.set_bypass_temperature_from_dwelling(23.5)
    await coordinator.async_shutdown()  # cancel the debouncer's pending cooldown timer

    brink.set_bypass_temperature_from_dwelling.assert_awaited_once_with(23.5)
    assert coordinator.bypass_temperature_from_dwelling == 23.5


async def test_set_bypass_temperature_from_outside_writes_through_and_refreshes(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    brink.get_bypass_temperature_from_outside = AsyncMock(return_value=9.5)
    coordinator._brink = brink

    await coordinator.set_bypass_temperature_from_outside(9.5)
    await coordinator.async_shutdown()  # cancel the debouncer's pending cooldown timer

    brink.set_bypass_temperature_from_outside.assert_awaited_once_with(9.5)
    assert coordinator.bypass_temperature_from_outside == 9.5


async def test_set_bypass_temperature_hysteresis_writes_through_and_refreshes(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    brink.get_bypass_temperature_hysteresis = AsyncMock(return_value=1.5)
    coordinator._brink = brink

    await coordinator.set_bypass_temperature_hysteresis(1.5)
    await coordinator.async_shutdown()  # cancel the debouncer's pending cooldown timer

    brink.set_bypass_temperature_hysteresis.assert_awaited_once_with(1.5)
    assert coordinator.bypass_temperature_hysteresis == 1.5


async def test_set_bypass_boost_writes_through_and_updates_state(hass):
    coordinator = BrinkHrvModbusCoordinator(hass)
    brink = _mock_brink()
    coordinator._brink = brink

    await coordinator.set_bypass_boost(1)

    brink.set_bypass_boost.assert_awaited_once_with(1)
    assert coordinator.bypass_boost == 1
