"""The main flask app"""

from flask import Flask, jsonify, request
from flask_expects_json import expects_json

from neo_pixel.neo import create_neo_pixel


app = Flask(__name__, static_url_path="") # Flask app
neo = None  # Neo pixel connection var

BRIGHTNESS_KEY = "brightness"


def _post_data() -> dict:
    """The json data sent via a POST

    Returns:
        dict: The POST data
    """
    default_brightness = 0.8
    post_data = request.get_json()
    if BRIGHTNESS_KEY not in post_data.keys():
        post_data[BRIGHTNESS_KEY] = default_brightness

    return post_data


@app.route("/test", methods=["GET"])
def test_page() -> str:
    """Test page for the system"""
    return "<h1>NEO PIXEL INTERFACE TEST PAGE</h1>"


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

    try:

        post_data = _post_data()
        neo.brightness = post_data[BRIGHTNESS_KEY]
        neo.fill(post_data["rgb"])
        neo.show()
        return_resp["success"] = True

    except Exception as ex:
        return_resp["success"] = False
        return_resp["error"] = str(ex)

    return jsonify(return_resp)


if __name__ == "__main__":
    with create_neo_pixel() as neo:
    	app.run(host="0.0.0.0", port=8082, debug=False)
