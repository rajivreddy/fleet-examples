import requests
import json

# Set your Rancher server URL and token
RANCHER_URL = "https://rancher.local"  # e.g., https://rancher.example.com
CLUSTER_ID = "c-m-j74kwf7s"
API_TOKEN = "token-rl2ws:xxxx"  # Rancher API token

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

def list_clusters():
    """
    Lists all clusters in Rancher.
    """
    url = f"{RANCHER_URL}/v3/clusters"
    response = requests.get(url, headers=headers, verify=True)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching clusters: {response.status_code} {response.text}")
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
    #List all clusters
    clusters = list_clusters()
    if not clusters:
        print("No clusters found.")
        exit(1)
    else:
        print("Clusters found:")
        for cluster in clusters:
            print(f" - {cluster['id']} : {cluster['name']} -- {cluster['state']}")
            print(f"   Labels: {cluster['labels'] if 'labels' in cluster else 'No labels'}")
    
    # Fetch the cluster Data
    cluster_data = get_cluster(CLUSTER_ID)
    if not cluster_data:
        print("Failed to fetch cluster data.")
        exit(1)
    print(f"Cluster data fetched for {CLUSTER_ID}: {cluster_data['name']}-- {cluster_data['state']}")
    
    ### Update the cluster labels 
    update_cluster_labels(CLUSTER_ID, cluster_data, "env", "test")  # Update the label
    
