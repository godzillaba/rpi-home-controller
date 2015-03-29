# rpi-home-automation-server
home automation stuff for gpio on your Raspberry Pi

### Usage
Connect to socket (by default listens on 0.0.0.0:5432) by means of telnet or a python script or something.

```PIN=<pin number>,OUT,1``` - Toggles a pin HIGH

```PIN=<pin number>,OUT,0``` - Toggles a pin LOW

```PIN=<pin number>,IN,0``` - Returns current state of pin (ex if pin 40 is high it will return 1)

#### Android
Now ```client/android-client.sh``` can be used to control your pi using your android device! The possibilities are virtually endless with all of tasker's various conditions (GPS, Wi-Fi, etc)! Requires busybox and netcat (nc)

#### NAT
If you wish to have control outside of your local network, you could use dmz host or port forwarding, but if you are like me and already have a media server or something as a dmz host, you can use ```proxy_server.py``` to relay your commands!

#### More to come...
* sensor support (temperature + humidity and all that good stuff)
* web interface
  * Camera support
* support for a button or switch to toggle pins
* organized alarm system or scheduling
  * ex turn on lights and or play music on chromecast as a sort of alarm in the morning
