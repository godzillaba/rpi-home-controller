# rpi-home-automation-server
home automation stuff for gpio on your Raspberry Pi

### Usage
Connect to socket (by default listens on 0.0.0.0:5432) by means of telnet or a python script or something.

```PIN=<pin number>,OUT,1``` - Toggles a pin HIGH

```PIN=<pin number>,OUT,0``` - Toggles a pin LOW

```PIN=<pin number>,IN,0``` - Returns current state of pin (ex if pin 40 is high it will return 1)

#### More to come...
In the future i will add a web interface, support for a button or switch to toggle pins, an organized alarm system or scheduling, and other stuff as it comes to mind.
