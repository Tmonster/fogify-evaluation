from ping_src.run_pings import run_ping_test
from bandwidth_src.run_bandwidth import run_bandwidth_test
from utils.enums import image_roles
import os


# TODO: parse image role from environment variable
def parse_image_role():
    try: 
        if os.environ["NODE_TYPE"] == "bandwidth_test":
            return image_roles.bandwidth_test
        return image_roles.ping_test
    except KeyError as e:
        return image_roles.bandwidth_test


def main():
    image_role = parse_image_role()

    if image_role == image_roles.bandwidth_test:
        run_bandwidth_test()

    if image_role == image_roles.ping_test:
        run_ping_test()
        

if __name__ == "__main__":
    main()
        
