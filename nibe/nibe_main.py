#43424, kompressorin kayntiaika lamminvesi 
#40008, menolampotila
#40012, paluulampotila
#40013, kayttovesi ylaosa
#43416, kompressori kaynnistykset
#40004, ulkolampotila
#43420, komressorinkayntiaika
#47265, puhallinnopeus
#40014, kayttoveden taytto
#40013, kayttovesi ylaosa

import sys
from pprint import pprint
from nibedownlink import NibeDownlink
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', '8086', 'grafana', 'grafana', 'home')

my_datapoint = {}
sensor_dict = {'outdoor': 40004, 'fanspeed': 47265, 'comp_time_warm_water': 43424, 'floor_water_in': 40008, 'floor_water_out': 40012, 'water_top': 40013, 'water_load': 40014  }

username = sys.argv[1]
password = sys.argv[2]
pumpid = sys.argv[3]

NIBE_UPLINK_CONF = {
  'username': username,
  'password': password,
  "hpid": pumpid,
  'variables': [43424,40008,40012,40013,43416,40004,43420,47265,40013,40014] # variables you want to fetch
}

nd = NibeDownlink(**NIBE_UPLINK_CONF)
online, values = nd.getValues()
print(values)

for key in sensor_dict:
   #print(key)
   #print(sensor_dict[key])
   my_datapoint["measurement"] = "NIBE-1245-8"
   my_datapoint["tags"] = {'sensor': key}
   my_datapoint["fields"] = {'value': (float((values[sensor_dict[key]])))}
   client.write_points([my_datapoint])

client.close()
