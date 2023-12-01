# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

from argparse import ArgumentParser

import RPi.GPIO as GPIO

mapping = {1: 16,
           2: 7,
           3: 8,
           4: 25}


def run():
    parser = ArgumentParser()
    parser.add_argument('ena_number', type=int, help='ENA',
                        choices=sorted(mapping.keys()))
    args = parser.parse_args()
    ena = args.ena_number
    gpio_high = mapping[ena]
    gpio_low = [mapping[x] for x in mapping.keys() if x != ena]
    print('Setting High: {}'.format(gpio_high))
    print('Setting Low: {}'.format(sorted(gpio_low)))

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(gpio_high, GPIO.OUT)
    GPIO.output(gpio_high, GPIO.HIGH)

    for c in gpio_low:
        GPIO.setup(c, GPIO.OUT)
        GPIO.output(c, GPIO.LOW)

