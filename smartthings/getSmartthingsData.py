#!/usr/bin/env python3
import aiohttp
import asyncio
import pysmartthings
import sys
import json
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', '8086', 'grafana', 'grafana', 'home')

token = sys.argv[1]
myGlobalData  = ""

async def get_devices():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        for device in devices:
            #print("{}: {}, {}".format(device.device_id, device.name, device.label))
            if device.name == "temp-pressure" or device.name == "humidity-temperature":
                await device.status.refresh()
                jsondata = device.status.values
                device_temperature = jsondata['temperature']
                device_humidity = jsondata['humidity']
                buildJson("temperature_" + device.label, device_temperature)
                buildJson("humidity_" + device.label, device_humidity)
            elif device.name == "single-switch-plug":
                await device.status.refresh()
                jsondata = device.status.values
                device_switch = jsondata['switch']
                if device_switch == "on":
                    device_switch = 1
                else:
                    device_switch = 0
                buildJson(device.label, float(device_switch))
            elif device.name == "Contact sensor with battery voltage (YG)":
                await device.status.refresh()
                jsondata = device.status.values
                device_contact = jsondata['contact']
                if device_contact == "open":
                    device_contact = 1
                else:
                    device_contact = 0
                buildJson("contact_" +device.label, float(device_contact))

        str = "[" + myGlobalData[:-1] + "]"
        dictData = json.loads(str)
        client.write_points(dictData)
        client.close()

def buildJson(device, value):
    global myGlobalData
    testjson = {
        "measurement": "Smartthings",
        "tags": {"sensor": device},
        "fields": {"value": value},
    }
    dict = json.dumps(testjson)
    myGlobalData = myGlobalData + dict + ","

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_devices())
    loop.close()

if __name__ == '__main__':
    main()
