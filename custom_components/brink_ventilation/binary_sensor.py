from .binary_sensors.filter_status_binary_sensor import FilterStatusBinarySensor

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    
    async_add_entities([
        FilterStatusBinarySensor(coordinator, entry.entry_id)
    ])


