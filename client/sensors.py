import paho.mqtt.client as mqtt
import time
import json
from envirophat import leds, light, weather

HOST_NAME = "10.1.1.1"
LOCATION = "FR-PAR-14L-4-PI"

class MeasurementBuilder:
    def __init__(self) -> None:
        self.measurement = None
        self.tags = {}
        self.values = {}
        self.timestamp = int(time.time() * 1000 * 1000 * 1000)

    def build(self) -> str:
        assert self.measurement != None
        assert len(self.values) != 0

        return "{},{} {} {}".format(self.measurement,
            ",".join(["{}={}".format(x, y) for x, y in self.tags.items()]),
            ",".join(["{}={}".format(x, json.dumps(y)) for x, y in self.values.items()]),
            self.timestamp)

def run():
    client = mqtt.Client()
    client.connect(HOST_NAME)
    client.loop_start()
    leds.off()
    topic = "sensors/" + LOCATION + "/environment"
    while True:
        builder = MeasurementBuilder()
        builder.measurement = "environment"
        builder.tags["location"] = "FR-TEST-PI"
        builder.values["temperature"] = weather.temperature()
        builder.values["pressure"] = weather.pressure()
        builder.values["light"] = light.light()
        print(builder.build())
        message = client.publish(topic, builder.build())
        time.sleep(10)

run()