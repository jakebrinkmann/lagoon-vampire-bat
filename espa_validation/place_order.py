"""Entry point to the retrieve_data.order_scenes_c1.py script"""

import argparse
from espa_validation.retrieve_data import order_scenes_c1


def main():
    parser = argparse.ArgumentParser(description=order_scenes_c1.__doc__)

    required_named = parser.add_argument_group("Required named arguments")

    required_named.add_argument("-u", dest="username", type=str, required=True, action="store",
                                help="ESPA user name")

    required_named.add_argument("-env", dest="espa_env", type=str, choices=["ops", "tst", "dev"], required=True,
                                action="store", help="ESPA environment")

    parser.add_argument("-o", dest="outdir", type=str, required=False, action="store",
                        help="Full path to the output directory")

    parser.add_argument("--ssl-verify", dest="ssl_ver", type=bool, required=False, action="store_true",
                        help="Set SSL Verify to True or False")

    parser.add_argument("--order", dest="order", type=str, required=False, action="store",
                        help="Specify a file containing an order in the form of a python dict() type.")

    args = parser.parse_args()

    order_scenes_c1.place_order(**vars(args))

    return None


if __name__ == "__main__":
    main()
