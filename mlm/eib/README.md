# Configure SELINUX and disable traefik ingress

this covers enabling `SELINUX` and disabling `traefik` with custom CIDR for cluster and services. you can find the configurrations in [server.yaml](./kubernetes/config/server.yaml)

```bash
build-eib --definition-file iso-definition.yaml
SELinux is enabled in the Kubernetes configuration. The necessary RPM packages will be downloaded.
Downloading file: rancher-public.key 100% |█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| (2.4/2.4 kB, 9.9 MB/s)
Setting up Podman API listener...
Generating image customization components...
Identifier ................... [SUCCESS]
Custom Files ................. [SKIPPED]
Time ......................... [SKIPPED]
Network ...................... [SKIPPED]
Groups ....................... [SKIPPED]
Users ........................ [SUCCESS]
Proxy ........................ [SKIPPED]
Resolving package dependencies...
Rpm .......................... [SUCCESS]
Os Files ..................... [SKIPPED]
Systemd ...................... [SKIPPED]
Fips ......................... [SKIPPED]
Elemental .................... [SKIPPED]
Suma ......................... [SKIPPED]
Populating Embedded Artifact Registry... 100% |███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| (14/14, 10 it/s)
Embedded Artifact Registry ... [SUCCESS]
Keymap ....................... [SUCCESS]
Configuring Kubernetes component...
Downloading file: k3s_installer.sh
Kubernetes ................... [SUCCESS]
Certificates ................. [SKIPPED]
Cleanup ...................... [SKIPPED]
Building ISO image...
Kernel Params ................ [SKIPPED]
Build complete, the image can be found at: eib-image.iso
```
