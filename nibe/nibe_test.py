import sys
from pprint import pprint
from nibedownlink import NibeDownlink

username = sys.argv[1]
password = sys.argv[2]
pumpid = sys.argv[3]

NIBE_UPLINK_CONF = {
  'username': username,
  'password': password,
  "hpid": pumpid, # heat pump id
  'variables': [10001] # variables you want to fetch
}

nd = NibeDownlink(**NIBE_UPLINK_CONF)
online, values = nd.getValues()
print(values)
