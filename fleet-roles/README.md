# Setting up Service Account
### Configure Service Account Token


```bash
kubectl apply -f admin.yaml
```

Create Service Account and associate service account token

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: fleet-admin-sa-token
  namespace: cattle-fleet-system
  annotations:
    kubernetes.io/service-account.name: fleet-admin-sa
type: kubernetes.io/service-account-token
EOF
````

Get the token associated with the Service Account

```bash
TOKEN=$(kubectl -n cattle-fleet-system get secret fleet-admin-sa-token -o jsonpath='{.data.token}' | base64 -d)
```
Use Curl

```bash
curl -s --cacert /path/to/ca.crt -H "Authorization: Bearer $TOKEN" https://{{ K8S-ENDPOINT }}/apis/fleet.cattle.io/v1alpha1/clusters
```

If youa are using KUBECONFIG

```
export KUBECONFIG=/root/fleet-config

kubectl config set-cluster default --server=https://k3s.local ### --certificate-authority=/root/custom-ca.crt (use this if your CA is not trusted with in system)
kubectl config set-credentials admin-user --token=$TOKEN
kubectl config set-context default --cluster=default --user=admin-user
kubectl config use-context default
```

```
kubectl config view --minify
```

```bash
kubectl get nodes
kubectl get pod -A
```
