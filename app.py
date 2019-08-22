#!/usr/bin/python

from flask import request
from flask_api import FlaskAPI
import R64.GPIO as GPIO
import config
import time

LEDS = {"trigger": 16}
#LEDS = {"green": 16}
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEDS["trigger"], GPIO.OUT)
#GPIO.setup(LEDS["red"], GPIO.OUT)

app = FlaskAPI(__name__)

@app.route('/', methods=["GET"])
def api_root():
    return {
           "led_url": request.url + "led/(trigger | green | red)/",
      		 "led_url_POST": {"state": "(0 | 1)"}
    			 }
  
@app.route('/led/<color>/', methods=["GET", "POST"])
def api_leds_control(color):
    if request.method == "POST":
        if color in LEDS:
            mod = (int(request.data.get("state")) + 1)%2
            GPIO.output(LEDS[color], int(request.data.get("state")))
            time.sleep ( 0.2 )
            GPIO.output(LEDS[color], int(mod))
            
    return {color: GPIO.input(LEDS[color])}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
