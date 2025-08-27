import os
import sys
import argparse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Usage: python upload_benchmark_result.py --file results.json --container benchmark-results --blob hetzner-01.json

def main():
    parser = argparse.ArgumentParser(description="Upload benchmark result to Azure Blob Storage.")
    parser.add_argument('--file', required=True, help='Path to the results file (json or zip)')
    parser.add_argument('--container', required=True, help='Blob container name')
    parser.add_argument('--blob', required=True, help='Blob name to use for upload')
    args = parser.parse_args()

    account_name = os.environ.get('AZURE_STORAGE_ACCOUNT')
    client_id = os.environ.get('AZURE_CLIENT_ID')
    tenant_id = os.environ.get('AZURE_TENANT_ID')
    client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    if not account_name:
        print("AZURE_STORAGE_ACCOUNT environment variable not set.")
        sys.exit(1)
    if not all([client_id, tenant_id, client_secret]):
        print("Azure SPN environment variables not set.")
        sys.exit(1)

    # Authenticate using ClientSecretCredential (SPN)
    from azure.identity import ClientSecretCredential
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    blob_url = f"https://{account_name}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=blob_url, credential=credential)

    container_client = blob_service_client.get_container_client(args.container)
    # Create container if it doesn't exist
    try:
        container_client.create_container()
    except Exception:
        pass  # Already exists

    # Upload the file
    with open(args.file, 'rb') as data:
        container_client.upload_blob(name=args.blob, data=data, overwrite=True)
    print(f"Uploaded {args.file} to container {args.container} as blob {args.blob}")

if __name__ == "__main__":
    main()
