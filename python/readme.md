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
                              

usage: cb-iot.py [-h] [-v] [-c CREDENTIALS] [-p PROJECT] [-r REGION] [-g REGISTRY] [-d DEVICE] [-n DEVICE_NUM_ID] [-o OPERATION] [-e EVENT_TOPIC] [-s STATE_TOPIC] [-k PUBLIC_KEY]
                 [-f PUBLIC_KEY_FORMAT]

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
  -n DEVICE_NUM_ID, --device-num-id DEVICE_NUM_ID
                        device num ID
  -o OPERATION, --operation OPERATION
                        operation: can be list, create, delete, get, device-list
  -e EVENT_TOPIC, --event-topic EVENT_TOPIC
                        event topic
  -s STATE_TOPIC, --state-topic STATE_TOPIC
                        state topic
  -k PUBLIC_KEY, --public-key PUBLIC_KEY
                        public key
  -f PUBLIC_KEY_FORMAT, --public-key-format PUBLIC_KEY_FORMAT
                        public key format (can be RSA_PEM, RSA_X509_PEM, ES256_PEM, ES256_X509_PEM)
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



