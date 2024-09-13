"""
Many Pico based boards with an network connection will require you to generate your
own mac addresses.
"""
from random import randint

def gen_mac() -> str:
    """Returns a random mac addres, in the raspi pi range"""
    return f"0xdc:0xa6:0x32:0x{randint(0, 255):02x}:0x{randint(0, 255):02x}:0x{randint(0, 255):02x}"

if __name__ == "__main__":
    print(gen_mac())
