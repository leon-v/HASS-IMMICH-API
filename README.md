## Home Assistant IMMICH API Integration
Curently only has sensors and switches for the Jobs queue.
I plan of tidying up the arcitecture to support smoother addition of other sensors.
Then will look at adding more endpoints.


Note to self - Hub has config objects - sensors impliment config
config objects live in huh, sensors live in sensors.py & switches.py
__init__.py
__pycache__/
.gitignore
api/
    __init__.py
    ImmichApi.py
    RestCommand.py
    RestEndpoint.py
    RestRequest.py
    RestValue.py
    RestValueBinary.py
components/
    __init__.py
    PolledCommandResponseSwitch.py
    NumberEntity.py
    BoolEntity.py
    SelectEntity.py
jobs/
    __init__.py
    Job.py
    Jobs.py
Constants.py
Exceptions.py
Hub.py
LICENSE
manifest.json
README.md
sensor.py
strings.json
switch.py

## Installation

Using the SSH addon run these commands:
```
cd /root/config/custom_components
git clone https://github.com/leon-v/HASS-IMMICH-API.git
ha host restart
```
Onece Home Assistant has restarted:
 - Settings -> Devices & Services
 - Add Integration
 - Search for 'IMMICH API' and click it
 - Enter your host name (e.g. http://192.168.100.61:2283)
 - Enter your API Key / Paste from IMMICH
 - - A new key can be created in IMMICH by clicking on an the administrator profile icon -> Account Settings -> API Keys -> New API Key, give the key a name like 'Home Assistant', click 'Create', Copy the key (Note: This is the only time the key will be presented)
 - Click 'Submit'
 - You will be presented with a success message if the connection test was successful.

From here you can search for the new sensors

## Links
 - https://github.com/home-assistant/example-custom-config/blob/master/custom_components/detailed_hello_world_push/__init__.py