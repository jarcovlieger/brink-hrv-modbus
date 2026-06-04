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
        self.filter_dirty = False
        self.modbus_contol_mode = 0  # 0=off, 1=switch, 2=flow rate value
        self.operating_hours = 0
        self.filter_used_in_hours = 0
        self.filter_used_in_cubic_meters_per_hour = 0
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
            self.fan_state = await self._brink.get_switch_position()
            self.filter_dirty = await self._brink.get_filter_dirty()
            self.modbus_contol_mode = await self._brink.get_modbus_control_switch_mode()
            self.operating_hours = await self._brink.get_operating_hours()
            self.filter_used_in_hours = await self._brink.get_filter_used_in_hours()
            self.filter_used_in_cubic_meters_per_hour = await self._brink.get_filter_used_in_cubic_meters_per_hour()
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

    async def reset_filter_warning(self) -> None:
        try:
            await self._brink.reset_filter_warning()
        except Exception as e:
            _LOGGER.error("Reset filter warning failed: %s", e)