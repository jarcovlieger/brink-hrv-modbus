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


def _brink_with_mock_holding_client(register_value: int) -> tuple[Brink, MagicMock]:
    """A Brink instance wired to a mock Modbus client for holding-register read/write."""
    brink = Brink(DEVICE_ID)
    client = MagicMock()
    result = MagicMock()
    result.registers = [register_value]
    client.read_holding_registers = AsyncMock(return_value=result)
    client.write_register = AsyncMock()
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


async def test_get_active_function_reads_correct_register():
    brink, client = _brink_with_mock_client(register_value=8)

    value = await brink.get_active_function()

    client.read_input_registers.assert_awaited_once_with(
        address=4020, count=1, device_id=DEVICE_ID
    )
    assert value == 8
async def test_get_bypass_mode_reads_correct_register():
    brink, client = _brink_with_mock_holding_client(register_value=2)

    value = await brink.get_bypass_mode()

    client.read_holding_registers.assert_awaited_once_with(
        address=6100, device_id=DEVICE_ID
    )
    assert value == 2


async def test_set_bypass_mode_writes_correct_register():
    brink, client = _brink_with_mock_holding_client(register_value=0)

    await brink.set_bypass_mode(1)

    client.write_register.assert_awaited_once_with(
        address=6100, value=1, device_id=DEVICE_ID
    )


async def test_get_bypass_boost_reads_correct_register():
    brink, client = _brink_with_mock_holding_client(register_value=1)

    value = await brink.get_bypass_boost()

    client.read_holding_registers.assert_awaited_once_with(
        address=6104, device_id=DEVICE_ID
    )
    assert value == 1


async def test_set_bypass_boost_writes_correct_register():
    brink, client = _brink_with_mock_holding_client(register_value=0)

    await brink.set_bypass_boost(1)

    client.write_register.assert_awaited_once_with(
        address=6104, value=1, device_id=DEVICE_ID
    )


@pytest.mark.parametrize(
    ("method_name", "address"),
    [
        ("get_bypass_temperature_from_dwelling", 6101),
        ("get_bypass_temperature_from_outside", 6102),
        ("get_bypass_temperature_hysteresis", 6103),
    ],
)
async def test_bypass_temperature_getter_reads_correct_register(method_name, address):
    brink, client = _brink_with_mock_holding_client(register_value=220)

    value = await getattr(brink, method_name)()

    client.read_holding_registers.assert_awaited_once_with(
        address=address, device_id=DEVICE_ID
    )
    assert value == 22.0


@pytest.mark.parametrize(
    ("method_name", "address"),
    [
        ("set_bypass_temperature_from_dwelling", 6101),
        ("set_bypass_temperature_from_outside", 6102),
        ("set_bypass_temperature_hysteresis", 6103),
    ],
)
async def test_bypass_temperature_setter_writes_scaled_value(method_name, address):
    brink, client = _brink_with_mock_holding_client(register_value=0)

    await getattr(brink, method_name)(22.5)

    client.write_register.assert_awaited_once_with(
        address=address, value=225, device_id=DEVICE_ID
    )
