"""Unit tests for the Brink Modbus client wrapper."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.brink_ventilation.lib.brink import Brink

DEVICE_ID = 20


def _brink_with_mock_client(register_value: int) -> tuple[Brink, MagicMock]:
    """A Brink instance wired to a mock Modbus client returning one register."""
    brink = Brink(DEVICE_ID)
    client = MagicMock()
    result = MagicMock()
    result.registers = [register_value]
    client.read_input_registers = AsyncMock(return_value=result)
    brink._client = client
    return brink, client


@pytest.mark.parametrize(
    ("method_name", "address"),
    [
        ("get_supply_fan_flow_setpoint", 4031),
        ("get_supply_fan_flow", 4032),
        ("get_exhaust_fan_flow_setpoint", 4041),
        ("get_exhaust_fan_flow", 4042),
    ],
)
async def test_flow_getter_reads_correct_register(method_name, address):
    brink, client = _brink_with_mock_client(register_value=350)

    value = await getattr(brink, method_name)()

    client.read_input_registers.assert_awaited_once_with(
        address=address, count=1, device_id=DEVICE_ID
    )
    assert value == 350


@pytest.mark.parametrize(
    "method_name",
    [
        "get_supply_fan_flow_setpoint",
        "get_supply_fan_flow",
        "get_exhaust_fan_flow_setpoint",
        "get_exhaust_fan_flow",
    ],
)
async def test_flow_getter_applies_no_scaling(method_name):
    """Unlike temperature registers, flow registers are already whole m3/h."""
    brink, _client = _brink_with_mock_client(register_value=123)

    value = await getattr(brink, method_name)()

    assert value == 123
