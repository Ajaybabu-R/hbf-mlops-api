from azure.keyvault.secrets import SecretClient
from app.core.identity import get_azure_credential
from app.core.config import settings


def get_secret_client():
    if not settings.KEY_VAULT_NAME:
        raise ValueError("KEY_VAULT_NAME not configured")

    vault_url = f"https://{settings.KEY_VAULT_NAME}.vault.azure.net"

    credential = get_azure_credential()

    return SecretClient(vault_url=vault_url, credential=credential)


def get_secret(secret_name: str) -> str:
    client = get_secret_client()
    secret = client.get_secret(secret_name)
    return secret.value