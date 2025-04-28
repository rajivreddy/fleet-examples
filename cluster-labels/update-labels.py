import requests
import json

# Set your Rancher server URL and token
RANCHER_URL = "https://rancher.loca"  # e.g., https://rancher.example.com
CLUSTER_ID = "c-m-xxxxxx"
API_TOKEN = "token-qwtzb:xxxxxxxxxxxx"  # Rancher API token

# Common headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}



def get_cluster(cluster_id):
    """
    Fetches the cluster object from Rancher.
    """
    url = f"{RANCHER_URL}/v3/clusters/{cluster_id}"
    response = requests.get(url, headers=headers, verify=True)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching cluster: {response.status_code} {response.text}")
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
        print("Cluster updated successfully!")
    else:
        print(f"Error updating cluster: {response.status_code} {response.text}")
        exit(1)


if __name__ == "__main__":
    # Fetch the cluster object
    cluster_data = get_cluster(CLUSTER_ID)
    if not cluster_data:
        print("Failed to fetch cluster data.")
        exit(1)
    
    update_cluster_labels(CLUSTER_ID, cluster_data, "env", "test")  # Update the label
    
