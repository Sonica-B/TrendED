import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

# Initialize logging
logging.basicConfig(level=logging.INFO)
# Retrieve connection string from environment variable
CONNECTION_STRING = os.getenv('AZURE_STORAGE_KEY')
if not CONNECTION_STRING:
    raise ValueError("Azure Storage connection string is not set.")

CONTAINER_NAME = "scraped-data"
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_to_blob(file_path, blob_name):
    """Upload a file to Azure Blob Storage."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        logging.info(f"File {file_path} uploaded as {blob_name}.")
        return f"File {blob_name} uploaded successfully."
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return f"Error uploading file: {e}"

def download_from_blob(blob_name, download_path):
    """Download a file from Azure Blob Storage."""
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        logging.info(f"Blob {blob_name} downloaded to {download_path}.")
        return f"File {blob_name} downloaded successfully."
    except ResourceNotFoundError:
        logging.error(f"Blob {blob_name} not found.")
        return f"Blob {blob_name} not found."
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return f"Error downloading file: {e}"


#
# def main():
#     # upload_to_blob("data/adzunaAPI_jobs.json", "adzunaAPI_jobs.json" )
#     download_from_blob("adzunaAPI_jobs.json", "data/test")