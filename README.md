# telloedu-mqtt

### Installation of related dependencies
```
$ pip install netifaces
$ pip install netaddr
```

### Python library for interfacing with the Ryze Tello Edu
from https://github.com/dwalker-uk/TelloEduSwarmSearch
There are three key files in the project:
* `fly_tello.py` - The `FlyTello` class is intended to be the only one that a typical user needs to use.  It contains functions enabling all core behaviours of one or more Tellos, including some complex behaviour such as searching for Mission Pads.  This should always be the starting point.
* `comms_manager.py` - The `CommsManager` class performs all of the core functions that communicate with the Tellos, sending and receiving commands and status messages, and ensuring they are acted on appropriately.  If you want to develop new non-standard behaviours, you'll probably need some of these functions.
* `tello.py` - The `Tello` class stores key parameters for each Tello, enabling the rest of the functionality.  The `TelloCommand` class provides the structure for both queued commands, and logs of commands which have already been sent.