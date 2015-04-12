# rpi-home-automation-server
home automation stuff for gpio on your Raspberry Pi

## Web Interface
Working demo <a href='http://therealtylerdurden.github.io/rpi-home-automation-server/html/'>here</a>

### Usage
The usage for the tcp and websocket servers are the same:

```PIN=<pin number>,OUT,1``` - Toggles a pin HIGH

```PIN=<pin number>,OUT,0``` - Toggles a pin LOW

```PIN=<pin number>,IN,0``` - Returns current state of pin (ex if pin 40 is high it will return 1)

```ALLRELAYS=1``` - Sets all relaypins high

#### Android
Now ```client/android-client.sh``` can be used to control your pi using your android device! The possibilities are virtually endless with all of tasker's various conditions (GPS, Wi-Fi, etc)!
###### Usage
```bash ./android-client.sh <pin> <1/0/->``` (- arg fetches current state and commands the opposite)
Requires busybox and netcat (nc)
