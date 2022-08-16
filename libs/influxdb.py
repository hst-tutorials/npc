#!/usr/bin/python3

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import configparser

configFile = os.path.abspath( os.path.dirname( __file__ ) ) + "/../config/config.ini"
config = configparser.ConfigParser()
config.read(configFile)

print(configFile)


def createInfluxClient():
    influxHost = config.get('influxdb', 'host')
    influxUsername = config.get('influxdb', 'username')
    influxToken = config.get('influxdb', 'token')
    influxOrg = config.get('influxdb', 'org')
    influxDatabase = config.get('influxdb', 'database')
    return InfluxDBClient(url=influxHost, token=influxToken, org=influxOrg)


def writeToInflux(data):

    influxHost = config.get('influxdb', 'host')
    influxUsername = config.get('influxdb', 'username')
    influxToken = config.get('influxdb', 'token')
    influxOrg = config.get('influxdb', 'org')
    influxDatabase = config.get('influxdb', 'database')

    with InfluxDBClient(url=influxHost, token=influxToken, org=influxOrg) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(influxDatabase, influxOrg, data)