from azure.identity import DefaultAzureCredential


def get_azure_credential():
    """
    Uses:
    - Managed Identity in Azure
    - Azure CLI locally
    - VS Code login
    Automatically picks best available credential.
    """
    return DefaultAzureCredential()