"""Place an ESPA order for potentially multiple scenes"""

# Modified from order_scenes_c1.py written by Steve Foga on 15 Aug 2014, modified by Steven Foga on 26 Jun 2017

import os
import sys
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests

from espa_validation.retrieve_data import api_config
from espa_validation.retrieve_data import espa_orders_api


def order_text(outdir: str) -> str:
    """
    Return a string containing the full path and filename of the text file to contain the order information
    :param outdir: The full path to the output directory, os.getcwd() by default if None is specified
    :return:
    """
    if outdir is None:
        outdir = os.getcwd()

    else:
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    return outdir + os.sep + "order_{}_.txt".format(api_config.timestamp())


def load_order(note: str, group: str='original') -> dict:
    """
    Load in a pre-constructed order by default if None is specified.  Otherwise, load the order from a .yaml file
    :param group: Group name to find orders (./orders/group/*.json)
    :param note: The order note (will become note.json)
    :return:
    """
    filename = 'espa_validation/orders/{group}/{note}.json'.format(group=group, note=note)
    if not os.path.exists(filename):
        raise IOError('File does not exist: {}'.format(filename))

    try:
        return json.load(open(filename))

    except Exception as exc:
        msg = "Problem loading file: {}".format(filename)
        print(msg)
        raise


def place_order(espa_env: str, username: str, ssl_ver: bool=True, outdir: str=None, group: str=None, note: str=None):
    """
    Place the order with the appropriate ESPA environment
    :param order: Optionally specify a keyword pointing to a specific order
    :param outdir: Optionally specify full path to the output directory, otherwise os.getcwd() is used
    :param ssl_ver: Depends on testing environment, True by default
    :param espa_env: The name of the ESPA environment
    :param username: ESPA username
    :return:
    """
    passwd = espa_orders_api.espa_login(username)

    espa_url = espa_orders_api.get_espa_env(espa_env)

    orders = load_order(note, group)

    order_length = len(orders)

    response = list()

    counter = 0

    for order in orders:
        counter += 1

        print("Requesting order {} of {}".format(counter, order_length))

        r = requests.post(espa_url + api_config.api_urls["order"],
                          auth=(username, passwd),
                          json=order,
                          verify=ssl_ver)

        try:
            response.append(r.json())

        except json.decoder.JSONDecodeError:  # inherits from ValueError
            # This error seems to occur when trying to decode a None-type object
            print("\nThere was likely a problem connecting with the host.  "
                  "Check to see if ESPA is down for maintenance.")

    if outdir:
        with open(order_text(outdir), "a") as f:
            if type(response) is dict:
                f.write(str(response) + "\n")

            else:
                for resp in response:
                    f.write(str(resp) + "\n")
    else:
        print(json.dumps(response, indent=4))

    return None
