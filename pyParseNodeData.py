#!/usr/bin/env python3
import requests
import json
import time
import sys
from influxdb import InfluxDBClient

CONFIG = {}
CONFIG['MAPURL'] = 'https://map.stormarn.freifunk.net/data/nodelist.json'
CONFIG['HOST'] = '127.0.0.1'
CONFIG['PORT'] = 8086
CONFIG['NEW'] = False
CONFIG['USER'] = 'python'
CONFIG['PASSWORD'] = ''
CONFIG['CLIENTSUM'] = True


def checkData(data):
    """
        Check if Data is in a healthy state
    """
    try:
        toplevel = data.keys()
        for key in ['version', 'nodes', 'updated_at']:
            if key not in toplevel:
                print("Missing key " + key)
                return False
        return True
    except KeyError as e:
        print("Error checking the data " + str(e))


def getData(url):
    """
        Loading the json file from the webserver
    """
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        with open('nodes.json', 'w') as outfile:
            try:
                json.dump(data, outfile)
                if(checkData(data)):
                    return data
                else:
                    return "error"
            except ValueError:
                return "error"
    else:
        return "error"


def parseData(data):
    """
        Parsing the json and extracting some metrics
    """
    dataList = []
    timestamp = int(time.time())
    clientsum = 0
    for entry in data['nodes']:
        node = {}
        node['measurement'] = "client_count"
        node['tags'] = {}
        node['tags']['id'] = str(entry['id'])
        node['tags']['name'] = str(entry['name'])
        node['time'] = timestamp
        node['fields'] = {}
        node['fields']['value'] = int(entry['status']['clients'])
        dataList.append(node)
        if CONFIG['CLIENTSUM']:
            clientsum += int(entry['status']['clients'])
    # Was to expensive to calc at db level
    if CONFIG['CLIENTSUM']:
        csum = {}
        csum['measurement'] = "client_sum"
        csum['time'] = timestamp
        csum['fields'] = {}
        node['fields']['value'] = clientsum
        dataList.append(csum)
    return dataList


def sendMessage(data):
    """
        Send the data points to the influxdb
    """
    client = InfluxDBClient(CONFIG['HOST'], CONFIG['PORT'], CONFIG['USER'], CONFIG['PASSWORD'], 'freifunk')
    # Optional
    # client.create_database('freifunk')
    client.write_points(data, 's')
    return "ok"  # "Result: {0}".format(result)


def main():
    global CONFIG
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            # Developer mode
            f = open("config.json.example", 'w')
            f.write(json.dumps(CONFIG, indent=4))
            sys.exit()
    try:
        configFile = open('config.json', 'r')
        config = json.load(configFile)
        CONFIG['MAPURL'] = str(config['MAPURL'])
        CONFIG['HOST'] = str(config['HOST'])
        CONFIG['PORT'] = int(config['PORT'])
        CONFIG['NEW'] = bool(config['NEW'])
        CONFIG['USER'] = str(config['USER'])
        CONFIG['PASSWORD'] = str(config['PASSWORD'])
        CONFIG['CLIENTSUM'] = bool(config['CLIENTSUM'])
    except ValueError as e:
        print("No config was found.")
        sys.exit()
    except KeyError as e:
        print("Setting not found: " + str(e))
        sys.exit()
    except FileNotFoundError as e:
        print("No config was found.")
        sys.exit()
    # When new file is needed
    if(CONFIG['NEW']):
        print('Loading new file')
        data = getData(CONFIG['MAPURL'])
        if data != "error":
            print(sendMessage(parseData(data)))
        else:
            print("error")
    else:
        print('Using old file')
        with open('nodes.json', 'r') as infile:
            data = json.load(infile)
            if(checkData(data)):
                print(sendMessage(parseData(data)))
            else:
                print("error")


if __name__ == '__main__':
    main()
