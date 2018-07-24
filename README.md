# Python wrapper for FutureNow IP relay/dimmer units

Usage example
```
import pyfnip
import random
import time

host = "192.168.1.199"
port = 7078
channel = 3

output = pyfnip.FNIP8x10aOutput(host, port, channel)

output.turn_on()
time.sleep(2)
output.turn_off()
```
