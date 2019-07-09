import paho.mqtt.client as mqtt
import time
import json
import bme680

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
    topic = "sensors/" + LOCATION + "/environment"

    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except IOError:
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    while True:
        sensor.get_sensor_data()

        builder = MeasurementBuilder()
        builder.measurement = "environment"
        builder.tags["location"] = "FR-TEST-PI"
        builder.values["temperature"] = sensor.data.temperature
        builder.values["pressure"] = sensor.data.pressure * 100.0 # Convert to Pascals
        builder.values["humidity"] = sensor.data.humidity
        print(builder.build())
        message = client.publish(topic, builder.build())
        time.sleep(10)

run()