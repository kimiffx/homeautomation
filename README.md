# homeautomation

influxdb install
```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update && sudo apt install -y influxdb
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service
```

create user to influxdb
```
create database home
use home
create user grafana with password '<enteryourpassword>' with all privileges
grant all privileges on home to grafana
```

enable auth ( auth-enabled = true )
```
sudo nano /etc/influxdb/influxdb.conf
sudo systemctl restart influxdb
```

testing auth
```
influx -username grafana -password <password>
```

install grafana
```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update && sudo apt install -y grafana
sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service
```
