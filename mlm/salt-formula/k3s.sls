ensure_k3s_service_running:
  service.running:
    - name: k3s 
    - enable: True