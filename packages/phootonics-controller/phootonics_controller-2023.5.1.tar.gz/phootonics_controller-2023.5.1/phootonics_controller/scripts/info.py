# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

from pprint import PrettyPrinter

import pandas
import requests


def monitor(url='http://0.0.0.0:5000'):
    rsp = requests.get(url + '/info')
    rsp.raise_for_status()
    pp = PrettyPrinter(indent=1)
    pp.pprint(rsp.json()['monitoring'])


def csv(url='http://0.0.0.0:5000'):
    rsp = requests.get(url + '/info')
    rsp.raise_for_status()
    j = rsp.json()
    df = pandas.DataFrame.from_records(j['scan']['results'],
                                       columns=['active_cavity',
                                                'detector_voltage',
                                                'wavelength',
                                                'wavelength_set_point',
                                                'x',
                                                'x_set_point',
                                                'y',
                                                'y_set_point'])
    df.to_csv('outputfile.csv')


def info(url='http://0.0.0.0:5000'):
    rsp = requests.get(url + '/info')
    rsp.raise_for_status()
    pp = PrettyPrinter(indent=1)
    pp.pprint(rsp.json())


if __name__ == '__main__':
    csv(url='http://phootonix:5000')