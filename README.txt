This Script will load the list of Nodes from a given urls and send the parsed Data to a InfluxDB.
Currently only the number of clients is collected this might get expanded in future.
It has some options.

MAPURL => Url to the nodelist.json from your Freifunk community.
HOST => ip/hostname of your influxdb
PORT => port of the influxdb
NEW => if the script should load the file from the server or use the local file
USER => influxdb user
PASSWORD => influxdb password
CALC-SUM => if the script should calculate the sum (seems to be better than a db query)
