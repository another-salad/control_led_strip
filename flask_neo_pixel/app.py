import board

import neopixel

from pathlib import Path

from collections import namedtuple

from flask import Flask, jsonify, request
from flask_expects_json import expects_json


# NeoPixel config
PX_PIN = board.D18
NUM_PX = 30
ORDER = neopixel.GRB
BRIGHTNESS = 0.8
AUTO_WRITE = False

# NeoPixel Connection object var
NEO = None

# OTHER DEFAULTS
BRIGHTNESS_KEY = "brightness"

app = Flask(__name__, static_url_path="") # flask object


def _post_data() -> dict:
    """The json data sent via a POST

    Returns:
        dict: The POST data
    """
    post_data = request.get_json()
    if BRIGHTNESS_KEY not in post_data.keys():
        post_data[BRIGHTNESS_KEY] = BRIGHTNESS

    return post_data


def _create_neo_pixel(brightness: float) -> object:
    """
    Creates the Neo pixel object and returns it

    Args:
        brightness (float): 0 - 1.0

    Returns:
        object: The NeoPixel object
    """
    return neopixel.NeoPixel(PX_PIN, NUM_PX, auto_write=AUTO_WRITE, pixel_order=ORDER, brightness=brightness)


@app.route("/set_px", methods=["POST"])
def set_px() -> str:
    """NOT YET IMPLEMENTED

    Returns:
        str: json string
    """
    return jsonify({"success": False, "error": "Not implemented"})


set_all_schema = {
    "properties": {
        "rgb": {"type": "array"},
        BRIGHTNESS_KEY: {"type": "number"}
    },
    "required": ["rgb"]
}
@app.route("/set_all", methods=["POST"])
@expects_json(set_all_schema)
def set_all() -> str:
    """Sets all neopixels to the RGB values provided

    Returns:
        str: json string
    """
    return_resp = {}
    post_data = _post_data()

    try:

        NEO.brightness = post_data[BRIGHTNESS_KEY]
        NEO.fill(post_data["rgb"])
        NEO.show()
        return_resp["success"] = True

    except Exception as ex:
        return_resp["success"] = False
        return_resp["error"] = str(ex)

    return jsonify(return_resp)


if __name__ == "__main__":
    with _create_neo_pixel(0) as NEO:
    	app.run(host="0.0.0.0", port=8082, debug=False)
