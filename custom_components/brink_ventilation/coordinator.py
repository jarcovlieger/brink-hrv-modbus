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

    @classmethod
    async def initialize(cls, hass, host, port):
        self = cls(hass)
        self._brink = await Brink.initialize(host, port, 20)
        return self
    
    async def _async_update_data(self):
        try:
            self.supply_temperature = await self._brink.get_supply_fan_temperature()
            self.exhaust_temperature = await self._brink.get_exhaust_fan_temperature()
            self.fan_state = await self._brink.get_switch_position()
            self.filter_dirty = await self._brink.get_filter_dirty()
            self.modbus_contol_mode = await self._brink.get_modbus_control_switch_mode()
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