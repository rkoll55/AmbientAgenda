from azure.iot.device import IoTHubDeviceClient, Message
import logging
import json
import recog

CONNECTION_STRING = "HostName=deco3801.azure-devices.net;DeviceId=raspberrypi1;SharedAccessKey=jZKYxNL3AY5EuMBZF/p9YDUy54ClsFYStjhp/v8E4yg="

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

json_object = recog.write_to_temp(recog.box_recog('images/marked_template.png'), "user1", infile="json/template.json", outfile="json/output.json") #has default file paths
# push to cloud over here
print("we running")
client = iothub_client_init()
client.connect()


#the code to send
print(json_object)
print(str(json_object))
message = Message(str(json_object))
message.content_encoding = "utf-8"
message.content_type = "application/json"
client.send_message(message)