"""Config flow for the Brink HRV Modbus integration."""

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from pymodbus.exceptions import ConnectionException
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT, DEFAULT_NAME
from .lib.brink import Brink

class BrinkHraModbusConfigFlow(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})

            brink = None
            try:
                brink = await Brink.initialize(
                    user_input[CONF_HOST], user_input[CONF_PORT], 20
                )
            except ConnectionException:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data=user_input
                )
            finally:
                if brink is not None:
                    brink.close()

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
