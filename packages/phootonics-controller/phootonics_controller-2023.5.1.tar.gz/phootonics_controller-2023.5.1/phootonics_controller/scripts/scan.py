# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import itertools
from argparse import ArgumentParser
import logging
from time import sleep

import requests

import pandas

WL_INCREMENT = 1.0

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PHOOTONICS_URL = 'http://0.0.0.0:5000'


def scan():
    parser = ArgumentParser()
    parser.add_argument('-x', nargs='+', type=float)
    parser.add_argument('-y', nargs='+', type=float)
    parser.add_argument('-ampl_x', type=float, default=5)
    parser.add_argument('-ampl_y', type=float, default=5)
    parser.add_argument('-wl', type=float, required=False, default=None)
    parser.add_argument('-wl_step', type=float, required=False, default=WL_INCREMENT)
    parser.add_argument('-scan', type=str, choices=['default', 'fast'], required=True)
    parser.add_argument('-url', type=str, required=False, default=PHOOTONICS_URL)
    args=parser.parse_args()


    rsp = requests.get(args.url + '/info')
    rsp.raise_for_status()
    info = rsp.json()
    if info['scan_running']:
        parser.error('Scan command already running.')


    if args.scan == 'default':
        x_list = args.x
        y_list = args.y

        positions = list(itertools.product(x_list, y_list))

        params = {'positions': positions}

        if args.wl is not None:
            params['wavelength'] = args.wl
        else:
            params['wl_step'] = args.wl_step

        print('submitting: {}'.format(params))

        rsp = requests.post(args.url + '/scan/start/default',
                            json=params)
        if not rsp.status_code == 200:
            print(rsp.json())
            rsp.raise_for_status()
    elif args.scan == 'fast':
        rsp = requests.post(args.url + '/scan/start/fast',
                            json={'wl_step': args.wl_step,
                                  'amplitude_x': args.ampl_x,
                                  'amplitude_y': args.ampl_y})
        if not rsp.status_code == 200:
            print(rsp.json())
            rsp.raise_for_status()

    while True:
        sleep(1)
        rsp = requests.get(args.url + '/info')
        rsp.raise_for_status()
        info = rsp.json()
        print('Completed: {:.0%}'.format(info['scan']['runtime']['completed']))
        if not info['scan_running']:
            break

    rsp = requests.get(args.url + '/info')
    rsp.raise_for_status()
    info = rsp.json()

    if args.scan == 'default':

        df = pandas.DataFrame.from_records(info['scan']['results'],
                                           columns=['active_cavity',
                                                    'detector_voltage',
                                                    'wavelength',
                                                    'wavelength_set_point',
                                                    'x',
                                                    'x_set_point',
                                                    'y',
                                                    'y_set_point'])
    elif args.scan == 'fast':
        df = pandas.DataFrame.from_records(info['scan']['results'],
                                           columns=['active_cavity',
                                                    'detector_voltage',
                                                    'wavelength',
                                                    'wavelength_set_point',
                                                    'x',
                                                    'y'])

    df.to_csv('outputfile.csv')

if __name__ == '__main__':
    import requests
    import logging

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


    scan()





