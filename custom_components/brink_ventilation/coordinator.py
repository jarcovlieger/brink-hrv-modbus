import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from datetime import timedelta
from .lib.brink import Brink

_LOGGER = logging.getLogger(__name__)

class BrinkHrvModbusCoordinator(DataUpdateCoordinator):
    _brink: Brink

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="Brink HRV Modbus Coordinator",
            update_interval=timedelta(seconds=5),
        )
       
        self.supply_temperature = None
        self.exhaust_temperature = None
        self.fan_state = 0
        self.last_fan_position = 1
        self.bypass_status = 0  # 4050: 0=initialize, 1=open, 2=close, 3=open, 4=closed
        self.preheater_status = 0  # 4060: 0=initialize, 1=inactive, 2=active, 3=test mode
        self.preheater_capacity = 0  # 4061: 0-100 percentage of max capacity
        self.frost_status = 0  # 4070: frost state-machine code 0-16
        self.frost_heater_power = 0  # 4071: heater output 0-100 percent
        self.frost_fan_reduction = 0  # 4072: fan reduction 0-100 percent
        self.filter_dirty = False
        self.modbus_contol_mode = 0  # 0=off, 1=switch, 2=flow rate value
        self.standby_mode = 0  # readback of 8003: 0=not in standby, 1=in standby
        self.signal_output = 0  # 6170: 0=off, 1=filter warning, 2=error, 3=both
        self.operating_hours = 0
        self.filter_used_in_hours = 0
        self.filter_used_in_cubic_meters_per_hour = 0
        self.filter_warning_days = 0
        self.CO2_sensor_1_status = 0
        self.CO2_sensor_2_status = 0
        self.CO2_sensor_3_status = 0
        self.CO2_sensor_4_status = 0
        self.CO2_sensor_1 = 0
        self.CO2_sensor_2 = 0 
        self.CO2_sensor_3 = 0
        self.CO2_sensor_4 = 0

    @classmethod
    async def initialize(cls, hass, host, port):
        self = cls(hass)
        self._brink = await Brink.initialize(host, port, 20)
        return self
    
    async def _async_update_data(self):
        try:
            self.supply_fan_status = await self._brink.get_supply_fan_status()
            self.supply_temperature = await self._brink.get_supply_fan_temperature()
            self.supply_humidity = await self._brink.get_supply_fan_relative_humidity()
            self.exhaust_fan_status = await self._brink.get_exhaust_fan_status()
            self.exhaust_temperature = await self._brink.get_exhaust_fan_temperature()
            self.exhaust_humidity = await self._brink.get_exhaust_fan_relative_humidity()
            self.bypass_status = await self._brink.get_bypass_status()
            self.preheater_status = await self._brink.get_preheater_status()
            self.preheater_capacity = await self._brink.get_preheater_capacity()
            self.frost_status = await self._brink.get_frost_status()
            self.frost_heater_power = await self._brink.get_frost_heater_power()
            self.frost_fan_reduction = await self._brink.get_frost_fan_reduction()
            self.fan_state = await self._brink.get_switch_position()
            self.filter_dirty = await self._brink.get_filter_dirty()
            self.modbus_contol_mode = await self._brink.get_modbus_control_switch_mode()
            self.standby_mode = await self._brink.get_standby_mode()
            self.operating_hours = await self._brink.get_operating_hours()
            self.filter_used_in_hours = await self._brink.get_filter_used_in_hours()
            self.filter_used_in_cubic_meters_per_hour = await self._brink.get_filter_used_in_cubic_meters_per_hour()
            self.filter_warning_days = await self._brink.get_filter_warning_days()
            self.signal_output = await self._brink.get_signal_output()
            self.CO2_sensor_1_status = await self._brink.get_CO2_sensor_1_status()
            self.CO2_sensor_2_status = await self._brink.get_CO2_sensor_2_status()
            self.CO2_sensor_3_status = await self._brink.get_CO2_sensor_3_status()
            self.CO2_sensor_4_status = await self._brink.get_CO2_sensor_4_status()
            self.CO2_sensor_1 = await self._brink.get_CO2_sensor_1()
            self.CO2_sensor_2 = await self._brink.get_CO2_sensor_2()
            self.CO2_sensor_3 = await self._brink.get_CO2_sensor_3()
            self.CO2_sensor_4 = await self._brink.get_CO2_sensor_4()
        except Exception as e:
            _LOGGER.error("Modbus read failed: %s", e)

    async def set_switch_position(self, position: int):
        try:
            if self.modbus_contol_mode != 1:
                await self._brink.set_modbus_control_switch_mode(1)  # set to switch mode

            await self._brink.set_switch_position(position)

            if position > 0:
                self.last_fan_position = position
        except Exception as e:
            _LOGGER.error("Set fan flow rate failed: %s", e)

    async def set_standby_mode(self, value: int) -> None:
        """Write the standby command register 8003 (write 1=standby, 2=normal)."""
        try:
            await self._brink.set_standby_mode(value)

            self.standby_mode = 1 if value == 1 else 0
            self.async_update_listeners()
        except Exception as e:
            _LOGGER.error("Set standby mode failed: %s", e)

    async def set_signal_output(self, value: int) -> None:
        """Write the signal output setting register (6170)."""
        try:
            await self._brink.set_signal_output(value)

            # Optimistically reflect the new value and notify entities. We deliberately do
            # NOT force an immediate refresh: the unit applies this setting with a short
            # internal delay, so re-reading 6170 now returns the old value and snaps the
            # select back. The regular 5s poll confirms it once the unit has committed.
            self.signal_output = value
            self.async_update_listeners()
        except Exception as e:
            _LOGGER.error("Set signal output failed: %s", e)

    async def reset_filter_warning(self) -> None:
        try:
            await self._brink.reset_filter_warning()
        except Exception as e:
            _LOGGER.error("Reset filter warning failed: %s", e)

    async def set_filter_warning_days(self, days: int) -> None:
        try:
            await self._brink.set_filter_warning_days(days)
            await self.async_request_refresh()
        except Exception as e:
            _LOGGER.error("Set filter warning days failed: %s", e)