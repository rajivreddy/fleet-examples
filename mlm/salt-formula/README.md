# README

This Salt formula will register the node to the appropriate Fleet server based on the `hostname%4`.

**Example:**
If your hostname is `t68511rxk3s` then `68511%4`=`3`, This Edge Node will be registered to Fleet 3.

## How to use

You can use custom Salt formulas to automate tasks on the minion/edge node.

### Folder structure

1. `/srv/salt/<custom-formula-name>/`
   This folder holds the salt formula
2. `/srv/formula_metadata/<custom-formula-name>/`
   This folder holds the Form Data and metadata of Salt formula

#### Prep Salt Directories

```bash
mkdir -p /srv/salt/join-fleet
mkdir -p /srv/formula_metadata/join-fleet
```

Copy the contents of the metadata folder to `/srv/formula_metadata/join-fleet`.

Copy the contents of the formula folder to `/srv/salt/join-fleet`.


### Generate Cluster registration

Cluster registration tokens are needed for registering `fleet-agent` to `fleet-controller`

This will create cluster registration token with infinite time

```bash
cat > registration-token.yaml << "EOF"
kind: ClusterRegistrationToken
apiVersion: "fleet.cattle.io/v1alpha1"
metadata:
    name: fleet-token
    namespace: fleet-default
spec:
    # A duration string for how long this token is valid for. A value <= 0 or null means infinite time.
    ttl: 0h

EOF
```

```bash
kubectl apply -f registration-token.yaml
```

Once the cluster registration token is created, run:

```bash
kubectl get secret new-token -o 'jsonpath={.data.values.}' | base64 --decode > values.yaml
```

you can find the token in the values.yaml file

Create `token1`, `token2`, `token3` and `token4` in `files` dir. these files holds the cluster registration token value.

Copy `ca.pem` file to `files` dir in `/src/salt/join-fleet`.


Once the formula is loaded, you should be able to see it in the `Formulas` tab in MLM. While creating activation keys, make sure to check the `"Configuration File Deployment"` option to enable automatic execution of Salt formulas on new systems.
