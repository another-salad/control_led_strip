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

# OTHER DEFAULTS
brightness_key = "brightness"

app = Flask(__name__, static_url_path="") # flask object


def _post_data() -> dict:
    """[summary]

    Returns:
        dict: [description]
    """
    post_data = request.get_json()
    if brightness_key not in post_data.keys():
        post_data[brightness_key] = BRIGHTNESS

    return post_data


def _create_neo_pixel(brightness: float) -> object:
    """[summary]

    Args:
        brightness (float): [description]

    Returns:
        object: [description]
    """
    return neopixel.NeoPixel(PX_PIN, NUM_PX, auto_write=AUTO_WRITE, pixel_order=ORDER, brightness=brightness)


@app.route("/set_px", methods=["POST"])
def set_px() -> str:
    pass


set_all_schema = {
    "properties": {
        "rgb": {"type": "array"},
        brightness_key: {"type": "number"}
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

        neo = _create_neo_pixel(post_data[brightness_key])
        neo.fill(post_data["rgb"])
        neo.show()
        return_resp["success"] = True

    except Exception as ex:
        return_resp["success"] = False
        return_resp["error"] = str(ex)

    return jsonify(return_resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=False)
