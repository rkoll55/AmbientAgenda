from azure.iot.device import IoTHubDeviceClient, Message
import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import logging
import json

CONNECTION_STRING = "HostName=deco3801.azure-devices.net;DeviceId=raspberrypi1;SharedAccessKey=jZKYxNL3AY5EuMBZF/p9YDUy54ClsFYStjhp/v8E4yg="

def iothub_client_init():
	client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
	return client

if __name__ == '__main__':

	account_url = "https://cs110032002ba3931bf.blob.core.windows.net"
	default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
	blob_service_client = BlobServiceClient(account_url, credential=default_credential)

	# Create a local directory to hold blob data
	#local_path = "../../json/overlay.json"
	#os.mkdir(local_path)

	# Create a file in the local data directory to upload and download
	local_file_name = "overlay.json"
	upload_file_path = os.path.join("../../json", local_file_name)

	# Write text to the file
	#file = open(file=upload_file_path, mode='w')
	#file.write("Hello, World!")
	#file.close()

	# Create a blob client using the local file name as the name for the blob
	blob_client = blob_service_client.get_blob_client(container="deco3801-storage", blob=local_file_name)

	print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

	# Upload the created file
	with open(file=upload_file_path, mode="rb") as data:
		blob_client.upload_blob(data)



	"""
	print("we running")
	client = iothub_client_init()
	#client.connect()
	with open('../../json/overlay.json', 'r') as openfile:
		json_object = json.load(openfile)
	print(json_object)
	print(str(json_object))
	message = Message(str(json_object))
	message.content_encoding = "utf-8"
	message.content_type = "application/json"
	client.send_message(message)
	"""
	
