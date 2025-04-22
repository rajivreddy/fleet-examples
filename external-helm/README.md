## Fleet gitrepo config

```yaml
kind: GitRepo
apiVersion: fleet.cattle.io/v1alpha1
metadata:
  name: helm-external
  namespace: fleet-default
spec:
  repo: https://github.com/rajivreddy/fleet-examples.git
  branch: main
  paths:
  - external-helm
  targets:
  - name: edge
    clusterSelector:
      matchLabels:
        type: edge
  - name: alpha
    clusterSelector:
      matchLabels:
        type: alpha
```
