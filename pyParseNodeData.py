#!/usr/bin/env python3
import requests
import pickle
import socket
import os
import json

MAPURL = 'https://map.stormarn.freifunk.net/data/nodelist.json'
HOST = '0.0.0.0'
PORT = '2004'
NEW = True


def packMessage():
    payload = pickle.dumps(listOfMetricTuples, protocol=2)
    header = struct.pack("!L", len(payload))
    message = header + payload
    return message


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
    for entry in data['nodes']:
        pass


def sendMessage(data):
    connection = socket.create_connection((HOST, PORT))
    connection.send(data)
    connection.close()


def main():
    if(NEW):
        print('Loading new file')
        data = getData(MAPURL)
        if data != "error":
            parseData(data)
        else:
            print("error")
    else:
        print('Using old file')
        with open('nodes.json', 'r') as infile:
            data = json.load(infile)
        parseData(data)
        return data


if __name__ == '__main__':
    main()
