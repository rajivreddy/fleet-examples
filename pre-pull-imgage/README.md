
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: prepull-job
spec:
  template:
    spec:
      containers:
      - name: prepull
        image: your-registry.com/your-image:tag
        command: ["sleep", "1"]
      restartPolicy: Never
```
