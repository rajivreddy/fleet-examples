# Deploy Fleet Into RKE Cluster

RKE2 and K3S has Helm CRD, This can apply any manifest file that were in `/var/lib/rancher/rke2/server/manifests/` Directory.

```yaml
cat > /var/lib/rancher/rke2/server/manifests/fleet.yaml << "EOF"
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: fleet-crd
  namespace: kube-system
spec:
  chart: fleet-crd
  repo: https://rancher.github.io/fleet-helm-charts/
  targetNamespace: cattle-fleet-system
  createNamespace: true
---
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: fleet
  namespace: kube-system
spec:
  chart: fleet
  repo: https://rancher.github.io/fleet-helm-charts/
  targetNamespace: cattle-fleet-system

---
apiVersion: v1
kind: Namespace
metadata:
  name: fleet-default
EOF
```

This will create `fleet.yaml` file in `/var/lib/rancher/rke2/server/manifests/` dir.

Once the Cluster is up and Running, This will run an Kubernetes Job which will trigger helm install.

```bash
kubectl get pods -n kube-system | grep fleet

kube-system           helm-install-fleet-crd-vzv4c                           0/1     Completed           0          62s
kube-system           helm-install-fleet-mn8np                               0/1     Completed           4          2m17s
kube-system           helm-install-rke2-canal-p2f5d                          0/1     Completed           0          7m20s
```

After the Jobs are completed.

```bash
kubectl get pods -n cattle-fleet-system
NAMESPACE             NAME                                                   READY   STATUS              RESTARTS   AGE
cattle-fleet-system   fleet-agent-68b7444497-669zf                           0/1     Terminating         0          1s
cattle-fleet-system   fleet-agent-68b7444497-htgg2                           0/1     Terminating         0          1s
cattle-fleet-system   fleet-agent-68b7444497-qgxls                           0/1     ContainerCreating   0          1s
cattle-fleet-system   fleet-controller-68d6f9fc8f-jnbbm                      3/3     Running             0          27s
cattle-fleet-system   gitjob-5c89968965-9zfgl                                1/1     Running             0          27s
```

```bash
kubectl get ns | grep fleet

cattle-fleet-clusters-system             Active   6m43s
cattle-fleet-system                      Active   7m33s
cluster-fleet-local-local-1a3d67d0a899   Active   6m41s
fleet-default                            Active   13m
fleet-local                              Active   6m41s
```
