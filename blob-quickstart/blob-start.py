import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here

    account_url = "https://cs110032002ba3931bf.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    account_url = "https://cs110032002ba3931bf.blob.core.windows.net"
    local_path = ''
    local_file_name = 'overlay'


    download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.json', 'DOWNLOAD.txt'))
    container_client = blob_service_client.get_container_client(container="deco3801-storage") 
    print("\nDownloading blob to \n\t" + download_file_path)

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)


    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())
    
except Exception as ex:
    print('Exception:')
    print(ex)






