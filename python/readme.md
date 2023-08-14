# cb-iot

## Installation

`python3 -m pip install -r requirements.txt`

## Usage

```
      _           _       _   
  ___| |__       (_) ___ | |_ 
 / __| '_ \ _____| |/ _ \| __|
| (__| |_) |_____| | (_) | |_ 
 \___|_.__/      |_|\___/ \__|
                              

usage: cb-iot.py [-h] [-v] [-c CREDENTIALS] [-p PROJECT] [-r REGION] [-g REGISTRY] [-d DEVICE] [-o OPERATION] [-e EVENT_TOPIC]
                 [-s STATE_TOPIC]

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase the verbosity level
  -c CREDENTIALS, --credentials CREDENTIALS
                        ClearBlade Service Account credentials key (required)
  -p PROJECT, --project PROJECT
                        GCP project id (required)
  -r REGION, --region REGION
                        GCP PubSub region
  -g REGISTRY, --registry REGISTRY
                        registry name
  -d DEVICE, --device DEVICE
                        device name
  -o OPERATION, --operation OPERATION
                        operation: can be list, create, delete, get, device-list
  -e EVENT_TOPIC, --event_topic EVENT_TOPIC
                        event topic
  -s STATE_TOPIC, --state_topic STATE_TOPIC
                        state topic
```

## Examples

### List registries

```
./cb-iot.py -c auth/credentials.json -p PROJECT-NAME -r us-central1 -o list
```

### Get registry and show its configuration

```
./cb-iot.py -c auth/credentials.json -p PROJECT-NAME -r us-central1 -g REGISTRY-NAME -o get
```



