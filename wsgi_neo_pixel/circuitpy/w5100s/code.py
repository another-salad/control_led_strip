import board
import busio
import digitalio
import time
import json

# NeoPixel
import neopixel

# # WSGI SERVER
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import *
from adafruit_wsgi.wsgi_app import WSGIApp
import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

##SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSN = board.GP17

##reset
W5X00_RSTN = board.GP20

def _get_config():
    """Gets the config from config.json"""
    with open("config.json", "r", encoding="UTF-8") as json_file:
        return json.load(json_file)

def config_eth():
    """Configures the ethernet adaptor, return initialized ethernet object"""
    ethernet_rst = digitalio.DigitalInOut(W5X00_RSTN)
    ethernet_rst.direction = digitalio.Direction.OUTPUT
    chip_select_pin = digitalio.DigitalInOut(SPI0_CSN)
    spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

    # Reset W5500 first
    ethernet_rst.value = False
    time.sleep(1)  # From the example code, this apparently stops race conditions on some boards. I'm paranoid, so I'm leaving it in.
    ethernet_rst.value = True

    # Setup network from config.json file
    net_config = _get_config()
    if not net_config.get("mac", ""):
        raise Exception("Mac address must be present in config file!")

    mac_addr = tuple((int(x, 16) for x in net_config["mac"].split(":")))

    # Prints go into serial stdout (nice for debugging)
    if not net_config.get("ipv4_addr", ""):
        print("Assuming DHCP setup as no ip address specified in config file")
        eth = WIZNET5K(spi_bus, chip_select_pin, is_dhcp=True, mac=mac_addr, debug=False)
    else:
        print("Assuming manual network config as ip address is present in config file")
        missing_config = False
        formated_config = {}
        # Add the ipv4_addr here although we know its already present, this is the easiest way to format the value for eth.ifconfig()
        for required_key in ["ipv4_addr", "subnet_mask", "default_gateway", "dns"]:
            if not net_config.get(required_key, ""):
                print(f"Missing required config: {required_key}")
                missing_config = True
                continue

            formated_config[required_key] = tuple(int(x) for x in net_config[required_key].split("."))

        if missing_config:
            raise Exception("Please review config.json file!")

        eth = WIZNET5K(spi_bus, chip_select_pin, is_dhcp=False, mac=mac_addr, debug=False)
        eth.ifconfig = (
            formated_config["ipv4_addr"], formated_config["subnet_mask"], formated_config["default_gateway"], formated_config["dns"]
        )

    print("Chip Version:", eth.chip)
    print("MAC Address:", [hex(i) for i in eth.mac_address])
    print("IP address:", eth.pretty_ip(eth.ip_address))
    # Return initialized WIZNET5K ethernet
    return eth

def setup_server(eth, wsgi_app, listening_port=80):
    """Sets up the server"""
    requests.set_socket(socket, eth)  # Initialize a requests object with a socket and ethernet interface
    server.set_interface(eth)
    return server.WSGIServer(listening_port, application=wsgi_app)

# Setup eth, server and start it
eth = config_eth()
web_app = WSGIApp()
wsgi_server = setup_server(eth, web_app)
wsgi_server.start()

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 30
pixels = neopixel.NeoPixel(board.GP0, NUM_PIXELS)

def _set_pixels(data: dict) -> dict:
    resp = {"error_code": 0}
    try:
        pixels.brightness = data.get("brightness", 0.8)
        pixels.fill(data["rgb"])
        pixels.show()
    except Exception as exc:
        resp["error_code"] = 1
        resp["stderr"] = repr(exc)

    return resp

@web_app.route("/api/set_all", methods=["POST"])
def set_all(request):
    """Sets all the NeoPixels to the provided values"""
    req = json.loads(request.wsgi_environ["wsgi.input"].getvalue())
    resp = _set_pixels(req)
    return ("200 OK", [], [json.dumps(resp)])

@web_app.route("/api/day", methods=["GET"])
def day(_):
    resp = _set_pixels({"rgb": [0, 0, 250]})
    return ("200 OK", [], [json.dumps(resp)])

@web_app.route("/api/night", methods=["GET"])
def night(_):
    resp = _set_pixels({"rgb": [245, 0, 0]})
    return ("200 OK", [], [json.dumps(resp)])

@web_app.route("/api/off", methods=["GET"])
def off(_):
    resp = _set_pixels({"rgb": [0, 0, 0]})
    return ("200 OK", [], [json.dumps(resp)])

while True:  # main loop
    wsgi_server.update_poll()
    # Maintain DHCP lease
    eth.maintain_dhcp_lease()

