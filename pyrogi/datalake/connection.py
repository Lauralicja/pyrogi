from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv(".env")

credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
        account_url=os.getenv("ACCOUNT_URL"),
        credential=credential)