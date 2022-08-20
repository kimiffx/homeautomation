#!/usr/bin/env python3
import aiohttp
import asyncio
import pysmartthings
import sys
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', '8086', 'grafana', 'grafana', 'home')

token = sys.argv[1]
my_datapoint = {}
my_datapoint["measurement"] = "Smartthings"

async def get_devices():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        for device in devices:
            #print("{}: {}, {}".format(device.device_id, device.name, device.label))
            if device.name == "temp-pressure":
                await device.status.refresh()
                jsondata = device.status.values
                device_temperature = jsondata['temperature']
                device_humidity = jsondata['humidity']
                my_datapoint["tags"] = {'sensor': 'temperature_' + device.label }
                my_datapoint["fields"] = {'value': float(device_temperature)}
                client.write_points([my_datapoint])
                my_datapoint["tags"] = {'sensor': 'humidity_' + device.label }
                my_datapoint["fields"] = {'value': float(device_humidity)}
                client.write_points([my_datapoint])
            if device.name == "single-switch-plug":
                await device.status.refresh()
                jsondata = device.status.values
                device_switch = jsondata['switch']
                if device_switch == "on":
                    device_switch = 1
                else:
                    device_switch = 0
                my_datapoint["tags"] = {'sensor': device.label }
                my_datapoint["fields"] = {'value': float(device_switch)}
                client.write_points([my_datapoint])
            if device.name == "Contact sensor with battery voltage (YG)":
                await device.status.refresh()
                jsondata = device.status.values
                device_contact = jsondata['contact']
                if device_contact == "open":
                    device_contact = 1
                else:
                    device_contact = 0
                my_datapoint["tags"] = {'sensor': 'contact_' + device.label }
                my_datapoint["fields"] = {'value': float(device_contact)}
                client.write_points([my_datapoint])

        client.close()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_devices())
    loop.close()

if __name__ == '__main__':
    main()
