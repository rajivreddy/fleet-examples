write_temp_ca_for_helm:
  file.managed:
    - name: /tmp/ca.pem
    - source: salt://join-fleet/files/ca.pem
    - mode: 644
