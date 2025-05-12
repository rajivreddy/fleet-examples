# Update Rancher Cluster Labels

### Set environment variables

```bash
export RANCHER_URL="https://rancher.local"
export RANCHER_USERNAME="admin"
export RANCHER_PASSWORD="password"
```

**Notes:**

1. Login Endpoint does not allow you to set the expiration time for the token, Default is 15Hrs.
2. Every login Creates New token

This script has `delete_expired_tokens()` Function, it will delete any expired tokens in Rancher.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running script

```bash
python main.py
```
