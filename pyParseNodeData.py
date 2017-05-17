#!/usr/bin/env python3
import requests
import pickle
import socket

MAPURL = '' # https://map.stormarn.freifunk.net/data/nodelist.json
HOST = '0.0.0.0'
PORT = '2004'


def packMessage():
    payload = pickle.dumps(listOfMetricTuples, protocol=2)
    header = struct.pack("!L", len(payload))
    message = header + payload
    return message


def getData(url):
    r = requests.get(url)
    data = r.json()
    return data


def parseData(data):
    for entry in data['nodes']:
        print()


def sendMessage(data):
    connection = socket.create_connection((HOST, PORT))
    connection.send(data)
    connection.close()


def main():
    parseData(getData(MAPURL))


if __name__ == '__main__':
    main()
