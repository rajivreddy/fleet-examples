{# Extract numeric part from hostname #}
{% set hostname = grains['host'] %}

{% set host_number_str = hostname | regex_replace('^.*?([0-9]+).*$', '\\1') %}
{% set host_number = host_number_str | int %}

{% set remainder = host_number % 4 %}

## Targeting First Fleet Server
{% if remainder == 0 %}
{% set fleet_server = "https://fleet-1.example.com/" %}

print_hostname:
  cmd.run:
    - name: echo {{ grains['id'] }}
# Copy Token from Master to Minion
copy_token:
  file.managed:
    - name: /tmp/token
    - source: salt://join-fleet/files/token-1
    - mode: 600

## Targeting Second Fleet Server
{% elif remainder == 1 %}
{% set fleet_server = "https://fleet-2.example.com/" %}

print_hostname:
  cmd.run:
    - name: echo {{ grains['id'] }}
# Copy Token from Master to Minion
copy_token:
  file.managed:
    - name: /tmp/token
    - source: salt://join-fleet/files/token-2
    - mode: 600


## Targeting Third Fleet Server
{% elif remainder == 2 %}
{% set fleet_server = "https://fleet-3.example.com/" %}

print_hostname:
  cmd.run:
    - name: echo {{ grains['id'] }}
# Copy Token from Master to Minion
copy_token:
  file.managed:
    - name: /tmp/token
    - source: salt://join-fleet/files/token-3
    - mode: 600


## Targeting Fourth Fleet Server
{% elif remainder == 3 %}
{% set fleet_server = "https://fleet-4.example.com/" %}

print_hostname:
  cmd.run:
    - name: echo {{ grains['id'] }}
# Copy Token from Master to Minion
copy_token:
  file.managed:
    - name: /tmp/token
    - source: salt://join-fleet/files/token-4
    - mode: 600

{% endif %}

### Run Helm Install/Upgrade Command 
install_or_upgrade_fleet_agent:
  cmd.run:
    - name: |
        TOKEN=$(cat /tmp/token)
        # echo $TOKEN
        helm --kubeconfig /etc/rancher/k3s/k3s.yaml -n cattle-fleet-system \
        upgrade --install --create-namespace --wait fleet-agent \
        https://github.com/rancher/fleet/releases/download/v0.12.3/fleet-agent-0.12.3.tgz \
          --set apiServerURL="{{ fleet_server }}" \
          --set clusterNamespace=fleet-default \
          --set token=$TOKEN \
          --set-file apiServerCA=/tmp/ca.pem
