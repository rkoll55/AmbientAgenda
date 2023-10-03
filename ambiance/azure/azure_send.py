from azure.iot.device import IoTHubDeviceClient, Message
import logging
import json

CONNECTION_STRING = "HostName=deco3801.azure-devices.net;DeviceId=raspberrypi1;SharedAccessKey=jZKYxNL3AY5EuMBZF/p9YDUy54ClsFYStjhp/v8E4yg="

def iothub_client_init():
	client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
	return client

if __name__ == '__main__':
	print("we running")
	client = iothub_client_init()
	#client.connect()
	with open('overlay.json', 'r') as openfile:
		json_object = json.load(openfile)
	print(json_object)
	print(str(json_object))
	message = Message(str(json_object))
	message.content_encoding = "utf-8"
	message.content_type = "application/json"
	client.send_message(message)
	
