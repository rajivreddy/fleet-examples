# Migrating Git Repos from Rancher to MLM

You can find all the gitrepos in `fleet-default` and `fleet-local` namespaces.

### Take a backup of Git Repos from Rancher

```bash
kubectl get gitrepo -n fleet-default -o yaml | yq 'del(.items[].status)' > all-repos.yaml
```

### Apply Gitrepos to Fleet Cluster

```bash
kubectl apply -f all-repos.yaml

```

### Remove Fleet-agent from the downstream cluster

```bash
helm uninstall fleet-agent-{{ CLUSTER_NAME}} -n cattle-fleet-system
```


### Register Existing Edge node to MLM

Make sure you are using right activation key in the Bootstrap script

```bash
curl -O {{FQDN_MLM}}/pub/bootstrap/{{ BOOTSTRAP_SCRIT }} | bash
```

Once the `venv-salt-minion` installed validate the status

```bash
systemctl status venv-salt-minion
```

Once the node registered to the MLM, `join-fleet` high state will run run automatically.

### Confirm the Edge cluster is registered to the Fleet cluster

```bash
kubectl get clusters -n fleet-default
````

Make sure labels are matching as per git repo configurations

```bash
kubectl get cluster {{ CLUSTER_NAME }} -n fleet-default -o yaml | yq '.metadata.labels'

```
confirm the labels are configured.

you should be able to see the the bundles are in sync.
