[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

[![GitHub Release](https://img.shields.io/github/release/jarcovlieger/brink-hrv-modbus.svg?style=for-the-badge&color=blue)](https://github.com/jarcovlieger/brink-hrv-modbus/releases) 

# Brink HRV Modbus Integration
Home Assistant integration to connect your Brink HRV (Heat Recovery Ventilation) to Home Assistant via Modbus TCP.

<img width="263" height="424" alt="Sensors_and_controls" src="https://github.com/user-attachments/assets/910c1447-eae7-4c51-8e0e-8c27c40aad29" />

## Hardware Setup
To connect your Brink HRV to Home Assistant via Modbus, a Modbus gateway device is needed. I'm using the [Waveshare RS485 to RJ45 Ethernet Module](https://www.waveshare.com/rs485-to-eth-b.htm?sku=23273) , but any arbitrary Modbus gatway should work.
<img width="1446" height="326" alt="brink-modbus-hardware-setup" src="https://github.com/user-attachments/assets/c97c82cb-86f1-40b0-8bbb-cf66a5bbaeda" />

1. Connect your Modbus Gateway to the same network as your Home Assistant instance
2. Connect the <b>RS485A</b> and the <b>RS485B</b> terminals to the corresponding terminals of your HRV (Check chapter 1.1 of [this document](https://www.brinkclimatesystems.nl/documenten/modbus-uwa2-b-uwa2-e-installation-regulations-614882.pdf))
3. Check the IP-address of your Modbus Gateway. (You can usually find this by logging into your router)
4. In your web browser navigate to the IP address of your Modbus gateway and login (default there is no password, so just press 'login')
5. Verify the required settings and submit them <img width="1918" height="1035" alt="afbeelding" src="https://github.com/user-attachments/assets/a2fb25c3-b146-483c-9349-e09ff10301e0" />
6. Note down the <b>device IP address</b> and <b>device port</b>. You will need this information when configuring the Home Assistant integration.

## Installation
To install the Brink HRV Modbus Integration, follow these steps:

#### HACS installation
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jarcovlieger&repository=brink-hrv-modbus=integration)

1. Go to the [HACS](https://hacs.xyz) panel
2. Go to integrations 
3. Search for 'Brink HRV Modbus'
4. Click \'Download this repository with HACS'.

#### Manual installation
1. Copy the ```brink_hrv_modbus``` folder into your ```custom_components``` folder

## Setup
1. Navigate to <b>Settings -> Devices & Services</b>
2. Click on <b>+ Add Integration</b>
3. Search for <b>"Brink HRV Modbus"</b>
4. Add in the <b>IP</b> of your modbus gateway and <b>port</b>

## Documentation
[modbus-uwa2-b-uwa2-e-installation-regulations-614882.pdf](https://www.brinkclimatesystems.nl/documenten/modbus-uwa2-b-uwa2-e-installation-regulations-614882.pdf)

## Tested devices
- Brink Flair 300
