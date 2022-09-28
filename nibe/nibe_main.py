#43424, kompressorin kayntiaika lamminvesi 
#40008, menolampotila
#40012, paluulampotila
#43416, kompressori kaynnistykset
#40004, ulkolampotila
#43420, komressorinkayntiaika
#47265, puhallinnopeus
#40014, kayttoveden taytto
#40013, kayttovesi ylaosa
#40025, poistoilma
#40026, jateilma
#40075, tuloilma
#40020, hoyrystin
#47212, teho sahkolisalampo
#10012, kompressori estetty
#43009, laskettu menolampotila

import sys
from pprint import pprint
from nibedownlink import NibeDownlink
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', '8086', 'grafana', 'grafana', 'home')

my_datapoint = {}
sensor_dict = {
   'BT1 Outdoor temperature': 40004,
   'Exhaust fan speed': 47265,
   'Total hot water operation time compr': 43424,
   'Floor water in': 40008,
   'Floor water out': 40012,
   'Water top': 40013,
   'Water load': 40014,
   'BT20 exhaust air temp': 40025,
   'BT21 vented air temp': 40026,
   'BT22 Supply air temp': 40075,
   'Compressor starts': 43416,
   'Total time compressor': 43420,
   'BT16 Evaporator temp': 40020,
   'Internal electrical addition power': 47212,
   'Compressor blocked': 10012,
   'Calc floor water supply': 43009
}

username = sys.argv[1]
password = sys.argv[2]
pumpid = sys.argv[3]

NIBE_UPLINK_CONF = {
  'username': username,
  'password': password,
  "hpid": pumpid,
  'variables': [43424,40008,40012,43416,40004,43420,47265,40013,40014,40025,40026,40075,40020,47212,10012,43009] # variables you want to fetch
}

nd = NibeDownlink(**NIBE_UPLINK_CONF)
online, values = nd.getValues()
print(values)

for key in sensor_dict:
   #print(key)
   #print(sensor_dict[key])
   my_datapoint["measurement"] = "Nibe"
   my_datapoint["tags"] = {'sensor': key}
   my_datapoint["fields"] = {'value': (float((values[sensor_dict[key]])))}
   client.write_points([my_datapoint])

client.close()
