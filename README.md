# npc - network performance checker
I created this small tool to quickly record my network performance and also have a long term display of all the collected data. The tool itself collects the data and is able to save it into an influxdb. The data then can be read and visualized by tools like grafana. For easier deployment, I created a docker image so you can pull the repository, execute the docker-compose file and get started. The script is designed to run on small devices like a raspberry pi but can also be run on any docker-host.

## Features:
- monitor network latency to multiple host
- fetch results from 3 different speedtest services (speedtest.net, fast.com and iPerf3)
- quickly save the results into an influxdb
- possibility to switch every feature on and off

# Setup:
## Prerequisites:
- installed docker engine and docker-compose plugin (https://docs.docker.com/desktop/install/linux-install/)

## Installation:

### You can install npc using two ways:
### 1. Clone the repository and build it yourself:
- clone the git repository onto your local machine: *git clone https://github.com/hst-tutorials/npc.git*
- enter the directory: *cd npc*
- (optional) adjust the prebuilt config file by editing app/config/config.json
- build the container using: *docker build . -t npc:latest*
- adjust the docker-compose file to use your custom created npc image
- start the stack using: *docker compose up -d*
- per default **no features** will be enabled as there are some key settings missing, more about that in the **config** section

### 2. Use the dockerhub image:
- create a docker-compose file and fill it with the following content:
    ```yml
    version: "3.9"
    services:
    grafana:
        image: grafana/grafana-oss:latest
        container_name: npc_grafana
        networks:
        - npc
        ports:
        - 3000:3000
        volumes:
        - grafana:/var/lib/grafana

    influxdb:
        image: influxdb:latest
        container_name: npc_influxdb
        networks:
        - npc
        ports:
        - 8086:8086
        volumes:
        - influxdb:/var/lib/influxdb2
        - influxdb_config:/etc/influxdb2

    app:
        image: hsttutorials/npc:latest
        container_name: npc_app
        networks:
        - npc
        volumes:
        - config.json:/app/config/config.json

    networks:
      npc:

    volumes:
      grafana:
      influxdb:
      influxdb_config:
    ```

    I really recommend using a reverse proxy like traefik or nginx in front of the two applications if you want to use the tool in a production environment.

- create a config.json and fill it like the one in the root directory of this repository
- start the stack using: *docker compose up -d*
- per default **no features** will be enabled as there are some key settings missing, more about that in the **config** section

After setting up the docker stack you need to configure the influxdb (if you want to use it of course, you can also use your own infrastructure if you like):
- Open the Web-UI of Influxdb (located at *hostname:8086*)
- Configure your default influxdb User:
![influxsetup](https://i.imgur.com/TqxwNQ5.png)
- Create some buckets for your features -> you can either use one bucket for each feature or use one for all. For better distinction between the different datasets, I recommend using multiple buckets
![influxbucket1](https://i.imgur.com/IRf3SgQ.png)
![influxbucket2](https://i.imgur.com/19LRv8C.png)
- Create an api-token for the application:
![influxapitoken1](https://i.imgur.com/7VZ2lhd.png)
![influxapitoken2](https://i.imgur.com/gfH1Qur.png)
Adjust the rights for the user to your likings, when your done, the api-key will be displayed and can be copied
- Edit the config.json to enable the influxdb feature and provide the needed arguments:
  ```json
  "influxdb": {
        "name": "influxdb",
        "enabled": true,
        "host": "http:/npc_influxdb:8086",
        "token": "yourToken",
        "org": "yourOrg"
    },
  ```
  If you downloaded the provided docker-compose, those settings should be enough to get your instance up and running.

## Configuration:
Every configuration is being made through changing the different keys in the config.json. Every feature can be enabled and disabled through the **enable** key which is present in every section. Every feature has some different settings, I explained them down below:

### Ookla speedtest (speedtest.net):
```json
    "ookla": {
        "name": "ookla",
        //state of the feature
        "enabled": false,
        //hostname used in the influx-queries
        "hostname": "speedtest.net",
        //name of your influxdb bucket
        "bucket": "npc_speedtest.net",
        //how often should we perform the check (in seconds)
        "interval": 60,
        //internal attributes used for identifying and configuring the module
        "args": ["config", "interval", "hostname", ""],
        "module": "libs.bandwidth.ookla"
    },
```

### iPerf3 speedtest:
```json
    "iperf3": {
        "name": "iperf3",
        //state of the feature
        "enabled": false,
        //name of your influxdb bucket
        "bucket": "npc_iperf3",
        //hostname of the iPerf3 server
        "hostname": "youriPerf3server.com",
        //port of the iPerf3 server
        "port": "5201",
        //how often should we perform the check (in seconds)
        "interval": 60,
        //internal attributes used for identifying and configuring the module
        "args": ["config", "interval", "hostname", "port"],
        "module": "libs.bandwidth.iPerf3"
    },
```
I recommend hosting a dedicated instance of the iPerf3 server (e.g. on a seperate port) as the iPerf server only can handle one connection at a time

### fast.com speedtest:
```json
    "fastCom": {
        "name": "fast.com",
        //state of the feature
        "enabled": false,
        //name of your influxdb bucket
        "bucket": "npc_fast.com",
        //hostname used in the influx-queries
        "hostname": "fast.com",
        //how often should we perform the check (in seconds)
        "interval": 60,
        //internal attributes used for identifying and configuring the module
        "args": ["config", "interval", "hostname", ""],
        "module": "libs.bandwidth.fastCom"
    },
```

### latency check:
```json
   "latency": {
        "name": "latency",
        //state of the feature
        "enabled": true,
        //list of hostnames to ping
        "hostnames": [
            "google.com", "fast.com"
        ],
        //how often should we ping the host
        "count": 4,
        //how often should we perform the check (in seconds)
        "interval": 0,
        //name of your influxdb bucket
        "bucket": "npc_latency",
        //internal attributes used for identifying and configuring the module
        "args": ["config", "interval", "hostnames", "count"],
        "module": "libs.ping.latency"
    }
```

After changing the config and restarting the app using *docker restart npc_app*, you should see data coming in. You can verify this using the built-in data explorer of influx:
!['influxexplorer](https://i.imgur.com/XSqAl7Y.png)

## Grafana dashboards:
After verifying, that data is being inserted into influxdb, you can start building your dashboards. If you're new to influxdb, a good approach is the data explorer where you can configure your queries by selecting the data you want to see. 
As grafana currently only supports you'll need to copy the resulting query (by changing the **query builder** to the **script editor**) in the data explorer. You will need those queries when creating your own grafana dashboards.

You can reach the grafana instance on port **:3000** of your docker host. After logging in with the default credentials (admin/admin) and changing your password, you first need to import a datasource:
![grafanaDatasource1](https://i.imgur.com/GvShhMl.png)
Select influxdb and enter the information as shown below:
![grafanaDatasource2](https://i.imgur.com/RZQ5Bt8.png)
![grafanaDatasource3](https://i.imgur.com/tMpzgrE.png)

After that you can save the source and start exploring. For some examples, I included my dashboard (examples/grafana.json) in the repository. You can import it using **Dashboards** > **Import** 
