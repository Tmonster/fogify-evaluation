from enum import Enum


class image_roles(Enum):
    ping_test = 1
    bandwidth_test = 2

class bandwidth_roles(Enum):
    server = 1
    client = 2