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
import argparse
from clearblade.cloud import iot_v1
from pyfiglet import *

def registry_list(project, region):
    client = iot_v1.DeviceManagerClient()

    request = iot_v1.ListDeviceRegistriesRequest(
        parent="projects/%s/locations/%s" % (project, region),
    )

    page_result = client.list_device_registries(request=request)

    for response in page_result:
        print(response.id, response.name)

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
            print(device.id, device.num_id, device.gateway_config['gatewayType'])
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
    parser.add_argument("-o", "--operation", default="", help="operation: can be list, create, delete, get, device-list")
    parser.add_argument("-e", "--event_topic", default="", help="event topic")
    parser.add_argument("-s", "--state_topic", default="", help="state topic")
    
    args = parser.parse_args()
    
    PROJECT_ID = args.project
    REGION_ID = args.region
    TARGET_REGISTRY_ID = args.registry
    TARGET_DEVICE_ID = args.device
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
                device_create(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
            case "delete":
                device_delete(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
            case "get":
                device_get(PROJECT_ID, REGION_ID, TARGET_REGISTRY_ID, TARGET_DEVICE_ID)
            
    else:
        print("Required options missing, please run the program with the -h option for further information.")

if __name__ == "__main__":
    main()