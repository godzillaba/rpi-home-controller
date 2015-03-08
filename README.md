# rpi-home-automation-server
home automation stuff for gpio on your Raspberry Pi

### API
To toggle pins high or low, you can use telnet or a python script to send "PIN=pin number,OUT,1 or 0"
To get the state of a pin (1 or 0), use the above syntax, replacing the OUT with IN, and the last number is arbitrary. ex) PIN=40,IN,0 will return 1 or 0
