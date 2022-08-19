from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from utils import logging as log


def writeToInflux(config, data, bucket):

    # use variables for better readablity
    influxHost = config['influxdb']['host']
    influxToken = config['influxdb']['token']
    influxOrg = config['influxdb']['org']

    # if the influxdb feature is enabled, connect to database and write given data into
    # given bucket
    if config['influxdb']['enabled'] == True:
        log.writeLog("Writing data to influxdb", "INFO", "stdout")
        with InfluxDBClient(url=influxHost, token=influxToken, org=influxOrg) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket, influxOrg, data)
    else:
        print(data)
