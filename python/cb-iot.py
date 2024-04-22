#!/usr/bin/env python3
"""
  cb-iot.py

  Operations on ClearBlade IoT-Core registries and devices

  [Usage] 
  python3 cb-iot.py [OPTIONS]
"""

__author__ = "Francesco Anselmo"
__copyright__ = "Copyright 2023"
__credits__ = ["Francesco Anselmo"]
__license__ = "APACHE 2.0"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo"
__email__ = "francesco.anselmo@gmail.com"
__status__ = "Dev"

import os
import io
import argparse
from clearblade.cloud import iot_v1
from pyfiglet import *

def registry_list(project, region):
    client = iot_v1.DeviceManagerClient()

    request = iot_v1.ListDeviceRegistriesRequest(
        parent="projects/%s/locations/%s" % (project, region),
    )

    page_result = client.list_device_registries(request=request)

    output = []
    for response in page_result:
        output.append(response.id)
        # print(response.id, response.name)
    print(output)
    print(output.sort())

def registry_create(project, region, registry_id, event_topic, state_topic):
    client = iot_v1.DeviceManagerClient()

    registry = iot_v1.DeviceRegistry(
        id=registry_id,
        mqttConfig={'mqttEnabledState':iot_v1.MqttState.MQTT_ENABLED},
        httpConfig={'httpEnabledState':iot_v1.HttpState.HTTP_DISABLED},
        logLevel=iot_v1.LogLevel.DEBUG,
        eventNotificationConfigs=[{'pubsubTopicName': event_topic}],
        stateNotificationConfig=[{'pubsubTopicName': state_topic}]
    )

    request = iot_v1.CreateDeviceRegistryRequest(
        parent="projects/%s/locations/%s" % (project, region),
        device_registry=registry
    )

    response = client.create_device_registry(request=request)

    try:
        print("Created registry %s:" % response.id)
        print('name: ', response.name)
        print('MQTT config:', response.mqtt_config['mqttEnabledState']) 
        print('HTTP config:', response.http_config['httpEnabledState'])
        print('Event topics:')
        for topic in response.event_notification_configs:
            print(' ', topic.pub_sub_topic_name)
        print('State topic:')
        print(' ', response.state_notification_config['pubsubTopicName'])
    except Exception as e:
        print(e)
        raise

def registry_delete(project, region, registry):
    project_id = project
    cloud_region = region
    registry_id = registry
    print("Delete registry %s" % registry)

    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    request = iot_v1.DeleteDeviceRegistryRequest(name=registry_path)
    try:
        client.delete_device_registry(request=request)
        print("Registry %s deleted" % registry_id)
        return "Registry deleted"
    except Exception as e:
        print(e)
        raise

def registry_get(project, region, registry):

    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(
        project,
        region,
        registry)

    request = iot_v1.GetDeviceRegistryRequest(
        name=registry_path,
    )

    response = client.get_device_registry(request=request)
    
    try:
        print("Get registry %s:" % response.id)
        print('name: ', response.name)
        print('MQTT config:', response.mqtt_config['mqttEnabledState']) 
        print('HTTP config:', response.http_config['httpEnabledState'])
        print('Event topics:')
        for topic in response.event_notification_configs:
            print(' ', topic.pub_sub_topic_name)
        print('State topic:')
        print(' ', response.state_notification_config['pubsubTopicName'])
    except Exception as e:
        print(e)
        raise

def device_list(project, region, registry):
    client = iot_v1.DeviceManagerClient()

    registry_path = client.registry_path(
        project,
        region,
        registry)

    request = iot_v1.ListDevicesRequest(parent=registry_path)

    response = client.list_devices(request=request)
    print("Showing devices for registry %s:" % registry)
    try:
        for device in response:
            #print(device.id, device.num_id, device.gateway_config['gatewayType'])
            print(device.id, device.num_id)
    except Exception as e:
        print(e)
        raise    

def device_get(project, region, registry, id):
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(
        project,
        region,
        registry,
        id)

    request = iot_v1.GetDeviceRequest(name=device_path)

    response = client.get_device(request)

    print(response)
    try:
        print("Get device %s:" % id, response.id, response.num_id, response.name)
    except Exception as e:
        print(e)
        raise

    return(response)


def device_create(project, region, registry, id):
    client = iot_v1.DeviceManagerClient()
    parent = client.registry_path(
        project,
        region,
        registry)

    device = iot_v1.Device(
        id=id, 
        gateway_config={"gatewayType": iot_v1.GatewayType.NON_GATEWAY},
        log_level=iot_v1.LogLevel.ERROR)
    
    request = iot_v1.CreateDeviceRequest(parent=parent, device=device)

    response = client.create_device(request)
    print(response)
    try:
        print("Created device %s:" % id, response.id, response.num_id, response.name)
    except Exception as e:
        print(e)
        raise
    
def device_create_numid(project, region, registry, id, numid):
    client = iot_v1.DeviceManagerClient()
    parent = client.registry_path(
        project,
        region,
        registry)

    device = iot_v1.Device(
        id=id, 
        num_id=numid,
        gateway_config={"gatewayType": iot_v1.GatewayType.NON_GATEWAY},
        log_level=iot_v1.LogLevel.ERROR)
    
    request = iot_v1.CreateDeviceRequest(parent=parent, device=device)

    response = client.create_device(request)
    print(response)
    try:
        # print("Created device %s:" % id, response.id, response.num_id, response.name)
        print("Created device %s:" % id)
    except Exception as e:
        print(e)
        raise

def device_unbind_from_gateway(project, region, registry, id, gateway):
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(
        project,
        region,
        registry)

    request = iot_v1.UnbindDeviceFromGatewayRequest(
        parent=parent,
        deviceId=id,
        gatewayId=gateway
    )
    response = client.unbind_device_from_gateway(request)
    print(response)

def device_update_numid(project, region, registry, id, numid):
    client = iot_v1.DeviceManagerClient()
    parent = client.registry_path(
        project,
        region,
        registry
    )

    device = iot_v1.Device(
        id=id, 
        num_id=numid
    )
    
    request = iot_v1.UpdateDeviceRequest(parent=parent, device=device, updateMask="numId")

    response = client.update_device(request)
    print(response)
    try:
        # print("Updated device %s:" % id, response.id, response.num_id, response.name)
        print("Updated device %s" % id)
    except Exception as e:
        print(e)
        raise

def device_update_key(project, region, registry, id, key, key_type):
    client = iot_v1.DeviceManagerClient()
    parent = client.registry_path(
        project,
        region,
        registry
    )

    key_format = iot_v1.PublicKeyFormat.RSA_PEM
    match key_type:
        case "RSA_PEM":
            key_format = iot_v1.PublicKeyFormat.RSA_PEM
        case "RSA_X509_PEM":
            key_format = iot_v1.PublicKeyFormat.RSA_X509_PEM
        case "ES256_PEM":
            key_format = iot_v1.PublicKeyFormat.ES256_PEM
        case "ES256_X509_PEM":
            key_format = iot_v1.PublicKeyFormat.ES256_X509_PEM

    with io.open(key) as f:
        public_key = f.read()

    device = iot_v1.Device(
        id=id, 
        credentials=[
            {
                "publicKey": {
                    "format": key_format,
                    "key": public_key,
                }
            }]
    )
    
    request = iot_v1.UpdateDeviceRequest(parent=parent, device=device, updateMask="credentials")

    response = client.update_device(request)
    print(response)
    try:
        # print("Updated device %s:" % id, response.id, response.num_id, response.name)
        print("Updated device public key %s" % id)
    except Exception as e:
        print(e)
        raise

    
def device_delete(project, region, registry, id):
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(
        project,
        region,
        registry,
        id)

    request = iot_v1.DeleteDeviceRequest(name=device_path)
    response = client.delete_device(request)
    try:
        print("Deleted device %s:" % id, response)
    except Exception as e:
        print(e)
        raise


def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText('cb-iot'))

def main():
      
    show_title()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="increase the verbosity level")  
    parser.add_argument("-c","--credentials", default="", help="ClearBlade Service Account credentials key (required)")
    parser.add_argument("-p","--project", default="", help="GCP project id (required)")
    parser.add_argument("-r","--region", default="us-central1", help="GCP PubSub region")
    parser.add_argument("-g", "--registry",  default="", help="registry name")
    parser.add_argument("-d", "--device", default="", help="device name")
    parser.add_argument("-n", "--device-num-id", default="", help="device num ID")
    parser.add_argument("-o", "--operation", default="", help="operation: can be list, create, delete, get, device-list")
    parser.add_argument("-e", "--event-topic", default="", help="event topic")
    parser.add_argument("-s", "--state-topic", default="", help="state topic")
    parser.add_argument("-k", "--public-key", default="", help="public key")
    parser.add_argument("-f", "--public-key-format", default="", help="public key format (can be RSA_PEM, RSA_X509_PEM, ES256_PEM, ES256_X509_PEM)")

    
    args = parser.parse_args()
    
    PROJECT_ID = args.project
    REGION_ID = args.region
    TARGET_REGISTRY_ID = args.registry
    TARGET_DEVICE_ID = args.device
    TARGET_DEVICE_NUMID = args.device_num_id
    TARGET_DEVICE_KEY = args.public_key
    TARGET_DEVICE_KEY_FORMAT = args.public_key_format
    OPERATION = args.operation
    os.environ["CLEARBLADE_CONFIGURATION"] = args.credentials
    
    if args.verbose:
        print("program arguments:")
        print(args)

    if args.credentials!="" and args.project!="" and args.region!="" and args.operation=="list":
        # List the registries
        registry_list(PROJECT_ID, REGION_ID)
        
    elif args.credentials!="" and args.project!="" and args.region!="" and args.registry !="" and args.device=="" and args.operation=="device-list":
        # List the devices in the target registry
        device_list(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID)

    elif args.credentials!="" and args.project!="" and args.region!="" and args.registry !="" and args.device=="" and args.operation!="":
        # Registry operations
        
        match OPERATION:
            case "create":
                if args.event_topic!="" and args.state_topic!="":
                    registry_create(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, args.event_topic, args.state_topic)
                else:
                    print("Please provide both an event and a state topic to create a registry.")
            case "delete":
                registry_delete(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID)
            case "get":
                registry_get(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID)
                
    elif args.credentials!="" and args.project!="" and args.region!="" and args.device!="" and args.operation!="":
        # Device operations
        
        match OPERATION:
            case "create":
                if TARGET_DEVICE_NUMID != "":
                    device_create_numid(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID, TARGET_DEVICE_NUMID)
                else:
                    device_create(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
            case "update":
                if TARGET_DEVICE_NUMID != "":
                    # device_update_numid(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID, TARGET_DEVICE_NUMID)
                    device_delete(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
                    device_create_numid(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID, TARGET_DEVICE_NUMID)
                if TARGET_DEVICE_KEY != "" and TARGET_DEVICE_KEY_FORMAT != "":
                    device_update_key(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID, TARGET_DEVICE_KEY, TARGET_DEVICE_KEY_FORMAT)
            case "delete":
                device_delete(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
            case "get":
                device_get(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
            
    else:
        print("Required options missing, please run the program with the -h option for further information.")

if __name__ == "__main__":
    main()
