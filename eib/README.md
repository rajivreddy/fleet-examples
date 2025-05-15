# Adding SELINUX package to EIB(standalone Image)

```bash
docker run --rm -it --privileged -v $CONFIG_DIR:/eib registry.suse.com/edge/3.2/edge-image-builder:1.1.1 build --definition-file iso-definition.yaml
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
Embedded Artifact Registry ... [SKIPPED]
Keymap ....................... [SUCCESS]
Configuring Kubernetes component...
Downloading file: k3s_installer.sh
Downloading file: k3s-airgap-images-amd64.tar.zst 100% |██████| (145/145 MB, 7.9 MB/s)
Downloading file: k3s 100% |█████████████████████████████████████| (71/71 MB, 7.9 MB/s)
Kubernetes ................... [SUCCESS]
Certificates ................. [SKIPPED]
Cleanup ...................... [SKIPPED]
Building ISO image...
Kernel Params ................ [SKIPPED]
Build complete, the image can be found at: eib-image.iso
```