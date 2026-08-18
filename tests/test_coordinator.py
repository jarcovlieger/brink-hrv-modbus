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
