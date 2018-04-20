"""Download orders using information returned from ESPA API. Creates sub-directories first by scene/product ID,
then by order note."""

# Modified from get_finished_espa_orders_api.py written by Steve Foga on 19 July 2016


import os
import ast
import requests
import getpass
import time
import datetime
from typing import Union
from pprint import pprint
from espa_validation.retrieve_data import api_config


def get_time() -> datetime.datetime:
    """
    Return the current time
    :return:
    """
    return datetime.datetime.now()


def espa_login(username: str=None) -> str:
    """
    Get ESPA password using command-line input
    :return:
    """
    return getpass.getpass("Enter ESPA password ({}): ".format(username))


def get_espa_env(env_in: str) -> str:
    """
    Return the URL based on the specified ESPA environment - a key to look up the URL from the
    api_config.espa_env dict
    :param env_in: ESPA environment
    :return:
    """
    return api_config.espa_env[env_in]


def check_order_status(product_id: str, base_url: str, username: str, password: str) -> Union[bool, str]:
    """
    Get information regarding whether or not an order is complete, return False if the order is incomplete
    :param product_id: The product ID
    :param base_url: ESPA URL for a specific environment
    :param username: ESPA username
    :param password: ESPA password
    :return:
    """
    r = requests.get(url=base_url + api_config.api_urls["status"] + product_id,
                     auth=(username, password))

    if product_id not in r.json():
        print("Error: order not found.")
        print("Return info: {}".format(r.json()))
        return

    else:
        status_info = r.json()[product_id]
        prod_stat = [str(item["status"]) for item in status_info]
        if all(status in ("complete", "unavailable") for status in prod_stat):
            print("Order ready to download")
            return status_info
        else:
            print("An error has occurred or orders have not yet finished.")
            return

from humanize import naturalsize as bytestr

def retrieve_order(outdir: str, order_url: str):
    """
    Download the order
    :param outdir: Full path to the order download folder
    :param order_url: Order download URL
    :return:
    """
    order_id = order_url.split("/")[-1]

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outfile = outdir + os.sep + order_id

    t = time.time()

    resp = requests.get(order_url, stream=True)

    print("{} [{}] --> {}".format(order_url, bytestr(resp.headers['Content-Length']), outfile))

    if resp.ok:
        with open(outfile, "wb") as f:
            for chunk in resp.iter_content(chunk_size=2048):
                f.write(chunk)

            if os.path.exists(outfile):
                print(os.path.getsize(outfile) / 1024 / (time.time() - t) / 1024)

    else:
        print("Could not download {}".format(order_url))
        print("Error {}".format(str(resp.status_code)))


def espa_list_orders(host, user, secret, status: str='complete'):
    # TODO: write docstring
    url = '{}/{}'.format(host, 'api/v1/list-orders')
    body = {'status': status}
    return [requests.get('{}/api/v1/order/{}'.format(host, o), auth=(user, secret)).json()
            for o in requests.get(url, json=body, auth=(user, secret)).json()]


def get_orders(txt_in: str, outdir: str, username: str, espa_env: str):
    """

    :param txt_in: The full path and filename of the input txt file containing the ESPA orders
    :param outdir: The full path to the output directory where orders will download to
    :param username: ESPA user name
    :param espa_env: ESPA environment
    :return:
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    passwd = 'LSRD_605today' # espa_login(username)
    espa_url = get_espa_env(espa_env)

    import json
    if txt_in:
        order_list = json.load(open(txt_in))
        order_list = filter(lambda x: 'errors' not in x, order_list)
    else:
        order_list = espa_list_orders(espa_url, username, passwd, ['complete', 'ordered'])

    urls = list()

    t0 = get_time()

    for order in order_list:

        if order["status"] == "complete" or order["status"] == "ordered":
            print("Getting order ID...")

            status_info = check_order_status(order["orderid"], espa_url, username, passwd)

            # print(order_info)

            if status_info is not None:
                scene_id = list()
                dl_url = list()

                order_info = requests.get(espa_url + api_config.api_urls["order"] + order["orderid"],
                                          auth=(username, passwd))

                note = str(order_info.json()["product_opts"].get("note") or 'note').capitalize()
                for j in status_info:
                    scene_id.append(j["name"])
                    if j['status'] == 'complete':
                        dl_url.append(j["product_dload_url"])

                if len(scene_id) > 2:
                    ord_sid = "multiple_" + scene_id[0]

                elif len(scene_id) > 1:
                    sid_sort = sorted(scene_id)

                    ord_sid = sid_sort[0] + "_" + sid_sort[1]

                else:
                    ord_sid = scene_id[0]

                for url in dl_url:
                    output_dir = outdir + os.sep + ord_sid + os.sep + note

                    retrieve_order(output_dir, url)

            else:
                print("Could not retrieve order {}.".format(order[u"orderid"]))

    t1 = get_time()

    print("Processing time: {}".format(t1 - t0))

    return None
