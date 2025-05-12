import requests
import json
import os
import time
import logging
import sys

# Set your Rancher server URL and token
RANCHER_URL = os.getenv("RANCHER_URL","https://ranche.local")
USERNAME = os.getenv("RANCHER_USERNAME", "admin")  # Rancher admin username
PASSWORD = os.getenv("RANCHER_PASSWORD", "admin")  # Rancher admin password
CLUSTER_ID = "c-m-j74kwf7sss"

# Common headers
headers = {
    "Content-Type": "application/json"
}

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG if needed
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def get_token():
    """
    Authenticates with Rancher and retrieves a token.
    """
    # API URL for Rancher authentication
    # This URL works for Local Authentication provider
    api_url = f"{RANCHER_URL}/v3-public/localProviders/local?action=login"
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    try:
        response = requests.post(api_url, json=payload, verify=True, headers=headers)
        response.raise_for_status()
        data = response.json()
        #This token will be expired after 16 hours
        return {
            "token": data["token"],
            "id": data["id"]
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Authentication failed: {e}")
        return None


def delete_token(token_id):
    """
    Deletes a token from Rancher.
    """
    api_url = f"{RANCHER_URL}/v3/token/{token_id}"
    try:
        response = requests.delete(api_url, verify=True, headers=headers)
        if response.status_code == 204:
            print("Token deleted successfully.")
        else:
            print(f"Failed to delete token: {response.status_code} {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to delete token: {e}")


def delete_expired_tokens():
    """
    Deletes expired tokens from Rancher.
    """
    api_url = f"{RANCHER_URL}/v3/tokens"
    try:
        response = requests.get(api_url, verify=True, headers=headers)
        if response.status_code == 200:
            tokens = response.json()["data"]
            for token in tokens:
                # Check if the token is expired
                if token["expired"] == True:
                    token_id = token["id"]
                    delete_token(token_id)
                    logging.info(f"Deleted expired token: {token_id}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch tokens: {e}")

def get_cluster(cluster_id):
    """
    Fetches the cluster object from Rancher.
    """
    url = f"{RANCHER_URL}/v3/clusters/{cluster_id}"
    print(f"Fetching cluster data from {url}")
    response = requests.get(url, headers=headers, verify=True)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching cluster data: {response.status_code} {response.text}")
        return None

def list_clusters():
    """
    Lists all clusters in Rancher.
    """
    url = f"{RANCHER_URL}/v3/clusters"
    response = requests.get(url, headers=headers, verify=True)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        logging.error(f"Error fetching clusters: {response.status_code} {response.text}")
        return None
    
def update_cluster_labels(cluster_id, cluster_data, label_key, label_value):
    """
    Updates the cluster object in Rancher.
    """
    # Update the labels in the cluster data
    if "labels" not in cluster_data:
        cluster_data["labels"] = {}
    ### Append the new label or Update the existing one

    cluster_data["labels"][label_key] = label_value
    
    url = f"{RANCHER_URL}/v3/clusters/{cluster_id}"
    response = requests.put(url, headers=headers, json=cluster_data, verify=True)
    if response.status_code == 200:
        logging.info(f"Cluster updated successfully")
    else:
        logging.error(f"Error updating cluster: {response.status_code} {response.text}")
        exit(1)


if __name__ == "__main__":
    # Get Cluster Token
    token_data = get_token()

    headers["Authorization"] = f"Bearer {token_data['token']}"
    
    delete_expired_tokens()
    
    clusters = list_clusters()
    if not clusters:
        logging.error("No clusters found.")
        exit(1)
    else:
        for cluster in clusters:
            print(f" - {cluster['id']} : {cluster['name']} -- {cluster['state']}")
            print(f"   Labels: {cluster['labels'] if 'labels' in cluster else 'No labels'}")
    
    # Fetch the cluster Data
    cluster_data = get_cluster(CLUSTER_ID)
    print(f"Cluster data fetched for {CLUSTER_ID} --> ClusterName: {cluster_data['name']} --> {cluster_data['state']}")
    
    ### Update the cluster labels 
    logging.info(f"Updating cluster labels for {CLUSTER_ID}")
    update_cluster_labels(CLUSTER_ID, cluster_data, "env", "prod")  # Update the label
    
