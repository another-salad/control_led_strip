#### Example usage:

##### /set_all
allows all of the RGB LEDs to be set to a colour

###### Happy path:
input: curl -X POST -H "Content-Type: application/json" -d '{"rgb": [140, 20, 180]}' http://IP:PORT/set_all  
resp: {"error":0}  

