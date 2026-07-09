from pymodbus.client import AsyncModbusTcpClient

class Brink():
    _client: AsyncModbusTcpClient = None 
    _device_id = 20

    def __init__(self, device_id = 20):
        self._device_id = device_id

    @classmethod
    async def initialize(cls, host, port, device_id):
        """Async factory method to return an initialized instance."""
        self = cls(device_id)
        self._client = AsyncModbusTcpClient(host, port=port)
        await self._client.connect()
        return self
    
    async def get_supply_fan_status(self) -> 'int':
        """
        Gets the supply fan status.
        :return: Fan status.
        """
        result = await self._client.read_input_registers(address=4030, count=1, device_id=self._device_id)
        return result.registers[0] 
    
    async def get_supply_fan_temperature(self) -> 'float':
        """
        Gets the supply fan temperature.
        :return: Temperature in degrees Celsius.
        """
        result = await self._client.read_input_registers(address=4036, count=1, device_id=self._device_id)
        return result.registers[0]/10.0 
    
    async def get_supply_fan_relative_humidity(self) -> 'int':
        """
        Gets the supply fan relative humidity.
        :return: Relative humidity in percentage.
        """
        result = await self._client.read_input_registers(address=4037, count=1, device_id=self._device_id)
        return result.registers[0] 
    
    async def get_bypass_status(self) -> 'int':
        """
        Gets the bypass status (register 4050).
        :return: 0 = Initialize, 1 = Open, 2 = Close, 3 = Open, 4 = Closed.
        """
        result = await self._client.read_input_registers(address=4050, count=1, device_id=self._device_id)
        return result.registers[0]

    async def get_exhaust_fan_status(self) -> 'int':
        """
        Gets the exhaust fan status.
        :return: Fan status.
        """
        result = await self._client.read_input_registers(address=4040, count=1, device_id=self._device_id)
        return result.registers[0] 
    
    async def get_exhaust_fan_temperature(self) -> 'float':
        """
        Gets the exhaust fan temperature.
        :return: Temperature in degrees Celsius.
        """
        result = await self._client.read_input_registers(address=4046, count=1, device_id=self._device_id)
        return result.registers[0]/10.0 
    
    async def get_exhaust_fan_relative_humidity(self) -> 'int':
        """
        Gets the exhaust fan relative humidity.
        :return: Relative humidity in percentage.
        """
        result = await self._client.read_input_registers(address=4047, count=1, device_id=self._device_id)
        return result.registers[0] 
    
    async def get_operating_hours(self) -> 'int':
        """
        Gets the operating time in hours.
        :return: Operating time in hours.
        """
        result = await self._client.read_input_registers(address=4113, count=2, device_id=self._device_id)
        
        if result.isError():
            raise RuntimeError(result)

        high_word = result.registers[0]
        low_word = result.registers[1]

        running_hours = (high_word << 16) | low_word

        return running_hours    

    async def get_filter_used_in_hours(self) -> 'int':
        """
        Gets the filter used in hours.
        :return: Filter used in hours.
        """
        result = await self._client.read_input_registers(address=4115, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_filter_used_in_cubic_meters_per_hour(self) -> 'int':
        """
        Gets the filter used in cubic meters per hour.
        :return: Filter used in cubic meters per hour.
        """
        result = await self._client.read_input_registers(address=4116, count=2, device_id=self._device_id)
        
        if result.isError():
            raise RuntimeError(result)

        high_word = result.registers[0]
        low_word = result.registers[1]

        cubic_meters_per_hour = (high_word << 16) | low_word

        return cubic_meters_per_hour    
    
    async def get_CO2_sensor_1_status(self) -> 'int':
        """
        Gets the CO2 sensor 1 status.
        :return: CO2 sensor 1 status.
        """
        result = await self._client.read_input_registers(address=4200, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_1(self) -> 'int':
        """
        Gets the CO2 sensor 1.
        :return: CO2 sensor 1.
        """
        result = await self._client.read_input_registers(address=4201, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_2_status(self) -> 'int':
        """
        Gets the CO2 sensor 2 status.
        :return: CO2 sensor 2 status.
        """
        result = await self._client.read_input_registers(address=4202, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_2(self) -> 'int':
        """
        Gets the CO2 sensor 2.
        :return: CO2 sensor 2.
        """
        result = await self._client.read_input_registers(address=4203, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_3_status(self) -> 'int':
        """
        Gets the CO2 sensor 3 status.
        :return: CO2 sensor 3 status.
        """
        result = await self._client.read_input_registers(address=4204, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_3(self) -> 'int':
        """
        Gets the CO2 sensor 3.
        :return: CO2 sensor 3.
        """
        result = await self._client.read_input_registers(address=4205, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_4_status(self) -> 'int':
        """
        Gets the CO2 sensor 4 status.
        :return: CO2 sensor 4 status.
        """
        result = await self._client.read_input_registers(address=4206, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def get_CO2_sensor_4(self) -> 'int':
        """
        Gets the CO2 sensor 4.
        :return: CO2 sensor 4.
        """
        result = await self._client.read_input_registers(address=4207, count=1, device_id=self._device_id)
        return result.registers[0]
    
    async def set_modbus_control_switch_mode(self, value: int) -> None:
        """
        Sets the Modbus control switched on register.
        :param value: 0 = Off, 1 = switch, 2 = flow rate value
        """
        return await self._client.write_register(address=8000, value=value, device_id=self._device_id)
     
    async def get_modbus_control_switch_mode(self) -> None:
        """
        Gets the Modbus control switched on register.
        :return: 0 = Off, 1 = switch, 2 = flow rate value
        """
        result = await self._client.read_holding_registers(address=8000, device_id=self._device_id)
        return result.registers[0]
    
    
    async def set_switch_position(self, value: int) -> None:
        """
        Sets the switch position register.
        :param value: 0 = Holiday, 1 = Low, 2 = Medium, 3 = High
        """
        return await self._client.write_register(address=8001, value=value, device_id=self._device_id)

    async def get_switch_position(self) -> int:
        """
        Gets the switch position register.
        :return: 0 = Holiday, 1 = Low, 2 = Medium, 3 = High
        """
        result = await self._client.read_holding_registers(address=8001, device_id=self._device_id)
        return result.registers[0]

    async def get_standby_mode(self) -> int:
        """
        Gets the standby command register (8003). Readback is the actual standby status.
        :return: 0 = Not in standby, 1 = In standby.
        """
        result = await self._client.read_holding_registers(address=8003, device_id=self._device_id)
        return result.registers[0]

    async def set_standby_mode(self, value: int) -> None:
        """
        Sets the standby command register (8003).
        :param value: 0 = No action, 1 = Set standby, 2 = Set normal mode.
        """
        return await self._client.write_register(address=8003, value=value, device_id=self._device_id)

    async def get_filter_warning_days(self) -> int:
        """
        Gets the number of days before a filter warning is raised (register 6120).
        :return: Days before filter warning (1-365).
        """
        result = await self._client.read_holding_registers(address=6120, device_id=self._device_id)
        return result.registers[0]

    async def set_filter_warning_days(self, value: int) -> None:
        """
        Sets the number of days before a filter warning is raised (register 6120).
        :param value: Days before filter warning (1-365).
        """
        return await self._client.write_register(address=6120, value=value, device_id=self._device_id)

    async def get_signal_output(self) -> int:
        """
        Gets the signal output setting register (6170).
        :return: 0 = Off, 1 = Filter warning, 2 = Error status, 3 = Filter warning and error status.
        """
        result = await self._client.read_holding_registers(address=6170, device_id=self._device_id)
        return result.registers[0]

    async def set_signal_output(self, value: int) -> None:
        """
        Sets the signal output setting register (6170).
        :param value: 0 = Off, 1 = Filter warning, 2 = Error status, 3 = Filter warning and error status.
        """
        return await self._client.write_register(address=6170, value=value, device_id=self._device_id)

    async def get_filter_dirty(self) -> bool:
        """
        Gets the filter dirty status.
        :return: True if filter is dirty, False otherwise.
        """
        result = await self._client.read_input_registers(address=4100, count=1, device_id=self._device_id)
        return result.registers[0] == 1
    
    async def reset_filter_warning(self) -> None:
        """
        Resets the filter warning.
        """
        return await self._client.write_register(address=8010, value=1, device_id=self._device_id)
    
