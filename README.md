# Python wrapper for FutureNow IP relay/dimmer/window cover units

Usage with lights example
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

Usage with window cover example
```
import pyfnip
import time 

covers = pyfnip.FNIP4xshOutput("192.168.1.101", "7078", "3")

covers.set_percentage("50")
time.sleep(1)
covers.stop()
time.sleep(1)

covers.up()
time.sleep(2)
covers.down()

print(covers._state)
```