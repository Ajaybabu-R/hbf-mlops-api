from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from app.core.identity import get_azure_credential
from app.core.config import settings


def get_blob_service_client():
    account_url = f"https://{settings.STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    credential = get_azure_credential()
    return BlobServiceClient(account_url=account_url, credential=credential)


def upload_text(container_name: str, blob_name: str, content: str):
    client = get_blob_service_client()
    blob_client = client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(content, overwrite=True)


def download_text(container_name: str, blob_name: str) -> str:
    client = get_blob_service_client()
    blob_client = client.get_blob_client(container=container_name, blob=blob_name)
    stream = blob_client.download_blob()
    return stream.readall().decode("utf-8")


def blob_exists(container_name: str, blob_name: str) -> bool:
    """
    Checks whether a blob exists in the given container.
    Used for idempotency protection.
    """
    try:
        client = get_blob_service_client()
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.get_blob_properties()
        return True
    except ResourceNotFoundError:
        return False