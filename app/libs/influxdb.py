#!/usr/bin/python3

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from . import getConfig as conf
from . import logging as log


def writeToInflux(data,bucket):
    config = conf.getConfig("configFile")

    influxHost = config['influxdb']['influxHost']
    influxToken = config['influxdb']['influxToken']
    influxOrg = config['influxdb']['influxOrg']

    with InfluxDBClient(url=influxHost, token=influxToken, org=influxOrg) as client:
        log.writeLog("Writing data to influxdb","INFO","stdout")
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, influxOrg, data)