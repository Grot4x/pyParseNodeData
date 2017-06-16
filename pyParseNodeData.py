#!/usr/bin/env python3
import requests
import json
import time
from influxdb import InfluxDBClient

MAPURL = 'https://map.stormarn.freifunk.net/data/nodelist.json'
HOST = '127.0.0.1'
PORT = '2004'
NEW = False
USER = 'python'
PASSWORD = ''
CALC-SUM = True

def checkData(data):
    toplevel = data.keys()
    for key in ['version', 'nodes', 'updated_at']:
        if key not in toplevel:
            print("Missing key " + key)
            return False
    return True

def getData(url):
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
    nodeList = []
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
        nodeList.append(node)
        if CLIENT-SUM:
            clientsum += int(entry['status']['clients'])
    if CLIENT-SUM:
        csum = {}
        csum['measurement'] = "client_sum"
        csum['time'] = timestamp
        nodeList.append(csum)
    return nodeList


def sendMessage(data):
    client = InfluxDBClient('localhost', 8086, USER, PASSWORD, 'freifunk')
    # Optional
    # client.create_database('freifunk')
    client.write_points(data, 's')
    return "ok"  # "Result: {0}".format(result)


def main():
    if(NEW):
        print('Loading new file')
        data = getData(MAPURL)
        if data != "error":
            print(sendMessage(parseData(data)))
        else:
            print("error")
    else:
        print('Using old file')
        with open('nodes.json', 'r') as infile:
            data = json.load(infile)
            if(checkData(data)):
                #print(sendMessage(parseData(data)))
                print("ok")
            else:
                print("error")

if __name__ == '__main__':
    main()
