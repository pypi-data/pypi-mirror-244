# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import logging

logger = logging.getLogger(__name__)

import RPi.GPIO as GPIO

mapping = {1: 16,
           2: 7,
           3: 8,
           4: 25}


def set_gpio_ena(ena):
    gpio_high = mapping[ena]
    gpio_low = [mapping[x] for x in mapping.keys() if x != ena]
    logger.info('Setting GPIO High: {}'.format(gpio_high))
    logger.info('Setting GPIO Low: {}'.format(sorted(gpio_low)))

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(gpio_high, GPIO.OUT)
    GPIO.output(gpio_high, GPIO.HIGH)

    for c in gpio_low:
        GPIO.setup(c, GPIO.OUT)
        GPIO.output(c, GPIO.LOW)
