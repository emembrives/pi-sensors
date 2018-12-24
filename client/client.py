import paho.mqtt.client as mqtt
import time
import json

HOST_NAME = "localhost"

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
    while True:
        builder = MeasurementBuilder()
        builder.measurement = "environment"
        builder.tags["location"] = "FR-TEST-PI"
        builder.values["temperature"] = 25
        builder.values["pressure"] = 1011
        print(builder.build())
        message = client.publish("sensors/FR-TEST-PI/environment", builder.build())
        time.sleep(2)

run()