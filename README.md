# netspeed
Shows an interface's (e.g. eth0) up/down speed in a linux machine (console application)

## usage

netspeed.py [-h] [--verbose] [--noclear] [interface]

## examples

```bash
netspeed.py # monitor default interface (eth0)
netspeed.py wlan0 # monitor wlan0
netspeed.py --noclear # monitor eth0 and do not clear the screen each second

```

