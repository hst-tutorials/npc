#!/usr/bin/python3

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def writeToInflux(config, data, bucket):
    influxHost = config['influxdb']['influxhost']
    influxToken = config['influxdb']['influxtoken']
    influxOrg = config['influxdb']['influxorg']

    with InfluxDBClient(url=influxHost, token=influxToken, org=influxOrg) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, influxOrg, data)
