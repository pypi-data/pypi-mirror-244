# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import logging
import os

os.environ['CONFIG_FILE'] = "/home/pi/ec_config/config_controller.json"

from phootonics_controller.base_controllers.main_controller import ADCDevice

logging.basicConfig(level=logging.DEBUG)


def read_hat():
    adc = ADCDevice()
    adc.initialise()
    print(adc.read_fast())
