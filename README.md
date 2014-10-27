# Python library to time data spent on various application easily from RescueTime API

official API documentation is here https://www.rescuetime.com/anapi/setup/documentation

## Example Usage

```
from rtlib import RescueTime

rt = RescueTime() # fetch today data in default
print rt.getTime(["Twitter"])
# 346.0

rt = RescueTime(beginDay="20141001",endDay="20141027")
print rt.getTime(["Twitter"],date="20141015")
# 832.0

```