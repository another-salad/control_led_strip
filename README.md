# control_led_strip
- Raspberry pi zero W
- Adafruit Neopixels (30 strip, configurable but untested)
- Flask interface for controlling Neopixels on RPI
- Flask interface for LDR (sub module project, used to control LEDs based on light readings)


## Due to limitations of using Neopixels and an RPI, the flask app must be ran as ROOT
### More info can be found here: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

### Additional note, it is stated in the above link, but please be aware of the following other RPI limiation:
----- NeoPixels must be connected to D10, D12, D18 or D21 to work (i.e board.DXX) -----

## Example usage:

### set_all
allows all of the RGB LEDs to be set to a colour

#### Happy path:
input: curl -X POST -H "Content-Type: application/json" -d '{"rgb": [140, 20, 180]}' http://IP:PORT/set_all
resp: {"success":true}

#### Sadness (invalid input value provided):
input: curl -X POST -H "Content-Type: application/json" -d '{"rgb": [100, 20, 300]}' http://IP:PORT/set_all
resp: {"error":"byte must be in range(0, 256)","success":false}
