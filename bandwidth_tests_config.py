bandwidth_tests_config = {
  "two_containers": {
    "yaml_file": "./yamls/bandwidth_tests/two_containers.yaml",
    "time": "60",
    "stagger": "true"
  },
  "two_containers_20mbps": {
    "yaml_file": "./yamls/bandwidth_tests/two_containers_20mbps.yaml",
    "time": "60",
    "stagger": "true"
  },
  "three_containers_concurrent": {
    "yaml_file": "./yamls/bandwidth_tests/three_containers.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "three_containers_concurrent_20mbps": {
    "yaml_file": "./yamls/bandwidth_tests/three_containers_20mbps.yaml",
    "time": "60",
    "concurrent": "true"
  },
  # "four_containers": {
  #   "yaml_file": "./yamls/bandwidth_tests/four_containers.yaml",
  #   "time": "60",
  #   "stagger": "true"
  # },
  "four_containers_concurrent": {
    "yaml_file": "./yamls/bandwidth_tests/four_containers.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "four_containers_concurrent_20mbps": {
    "yaml_file": "./yamls/bandwidth_tests/four_containers_20mbps.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "six_containers_concurrent": {
    "yaml_file": "./yamls/bandwidth_tests/six_containers.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "eight_containers_concurrent": {
    "yaml_file": "./yamls/bandwidth_tests/eight_containers.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "four_containers_two_networks": {
    "yaml_file": "./yamls/bandwidth_tests/bandwidth_test_2_networks.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "six_containers_three_networks": {
    "yaml_file": "./yamls/bandwidth_tests/bandwidth_test_3_networks.yaml",
    "time": "60",
    "concurrent": "true"
  },
  "six_containers_two_networks": {
    "yaml_file": "./yamls/bandwidth_tests/six_containers_two_networks.yaml",
    "time": "60",
    "concurrent": "true"
  }
}