# Setup HAProxy for HA RKE2 clusters

### install haproxy

```bash
# For rocky linux
dnf install haproxy -y
# for Ubuntu
apt-get update
apt-get install -y haproxy
```
### Configure HAProxy

create .pem/cert file for HAproxy

```bash
mkdir -p /etc/haproxy/certs
cat "private.key" "certificate.crt" /etc/haproxy/certs/certs.crt
ls -lthr /etc/haproxy/certs/
```

### update haproxy.cfg 

```
frontend kubernetes-api

    bind *:443 ssl crt /etc/haproxy/certs/cert.crt
    default_backend rke2_apiservers

backend rke2_apiservers
    balance roundrobin
    option tcp-check
    tcp-check connect
    server rke2-node1 $MASTER1_IP:6443 ssl verify none
    server rke2-node2 $MASTER2_IP:6443 ssl verify none
    server rke2-node3 $MASTER3_IP:6443 ssl verify none
```

### Configure Service Account Token

```bash
# If your certs are self signed
cp custom-ca.crt /usr/local/share/ca-certificates/
update-ca-certificates
```

Create Service Account and associate service account token

```
kubectl -n kube-system create sa admin-access
```

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: admin-access-token
  namespace: kube-system
  annotations:
    kubernetes.io/service-account.name: admin-access
type: kubernetes.io/service-account-token
EOF
````
Cluster Rolebinding

```bash
kubectl create clusterrolebinding admin-access \
  --clusterrole=cluster-admin \
  --serviceaccount=kube-system:admin-access
```

Get the token associated with the Service Account

```bash
TOKEN=$(kubectl -n kube-system get secret admin-access-token -o jsonpath='{.data.token}' | base64 -d)
```

Create New Kube configuration based on Service Account Token 

```
export KUBECONFIG=/root/rke2-config

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
