#!/usr/bin/env python3
import requests
import json
import time
from influxdb import InfluxDBClient

MAPURL = 'https://map.stormarn.freifunk.net/data/nodelist.json'
HOST = '127.0.0.1'
PORT = '2004'
NEW = True
USER = 'python'
PASSWORD = ''


def getData(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        with open('nodes.json', 'w') as outfile:
            json.dump(data, outfile)
        return data
    else:
        return "error"


def parseData(data):
    nodeList = []
    timestamp = int(time.time())

    for entry in data['nodes']:
        node = {}
        node['measurement'] = "client_count"
        node['tags'] = {}
        node['tags']['id'] = str(entry['id'])
        node['tags']['name'] = str(entry['name'])
        node['time'] = timestamp
        node['fields'] = {}
        node['fields']['value'] = str(entry['status']['clients'])
        nodeList.append(node)
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
            print(sendMessage(parseData(data)))


if __name__ == '__main__':
    main()
