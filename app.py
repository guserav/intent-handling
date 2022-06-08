from flask import Flask, request
import json
import paho.mqtt.client as mqtt
import time
import os

BROKER = "jackson"
TOPIC = "/topic/esp32_led"

os.environ['TZ'] = "CET"
time.tzset()

app = Flask(__name__)
@app.route('/', methods=["POST"])
def endpoint():
    data = request.json
    intent = data['intent']['name']
    print(json.dumps(data, indent=4))
    if intent == "ChangeLightState":
        if data['slots']['name'] == 'desk':
            client = mqtt.Client("Temperature_Inside")
            client.connect(BROKER)
            if data['slots']['state'] == 'on':
                client.publish(TOPIC, 'recover')
            else:
                client.publish(TOPIC, 'turnoff')
            client.disconnect()
        else:
            print("No idea")
            print(intent)
    elif intent == "GetTime":
        t = time.localtime()
        return {"speech": {"text": "The time is {:d} {:d}".format(t.tm_hour, t.tm_min)}}
    elif intent == "Division":
        t = time.localtime()
        n1 = data['slots']['num1']
        n2 = data['slots']['num2']
        print(n1, n2)
        return {"speech": {"text": "The result of {:d} divided by {:d} is {:0.2f}".format(n1, n2, n1/n2)}}
    else:
        return {"speech": {"text": "Sorry I couldn't understand you"}}
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
