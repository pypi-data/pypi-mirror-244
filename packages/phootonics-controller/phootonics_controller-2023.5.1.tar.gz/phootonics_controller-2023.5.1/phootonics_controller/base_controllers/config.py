import json
import logging
import os

import numpy

logger = logging.getLogger(__name__)

VCM_PORT = '/dev/tty.ec_vcm_main'
EXT_VCM_PORT = '/dev/tty.ec_vcm_ext'
LAST_POSITION = 1
LAST_CAVITY = 1
CAVITY1_INDEX = 'ec1'
CAVITY2_INDEX = 'ec2'
CAVITY3_INDEX = 'ec3'
CAVITY4_INDEX = 'ec4'
CAVITY1_URL = 'http://0.0.0.0:5001/ec/api/v1.0'
CAVITY2_URL = 'http://0.0.0.0:5002/ec/api/v1.0'
CAVITY3_URL = 'http://0.0.0.0:5003/ec/api/v1.0'
CAVITY4_URL = 'http://0.0.0.0:5004/ec/api/v1.0'

CAVITY_INDEXES = [CAVITY1_INDEX, CAVITY2_INDEX, CAVITY3_INDEX, CAVITY4_INDEX]

ADC_CHANNEL = 0
REF = 5.08  # Modify according to actual voltage (read voltage) external AVDD and AVSS (Default), or internal 2.5V

TEMP_STAB_TIMEOUT_SEC = 180


if 'CONFIG_FILE' not in os.environ:
    raise Exception('required configuration file path')

config_file_path = os.environ['CONFIG_FILE']

with open(config_file_path, 'r') as f:
    configuration_dictionary = json.load(f)

config_example = {'wavelength': [1037.2, 1353.6], 'x_position': -18.65, 'y_position': 0.5,
                  's2params': {'pulse_period': 6000, 'pulse_width': 300,
                               'pulsing_mode': 'internal', 'applied_voltage': 18.6,
                               'out_width': 100},
                  'temperature_setpoint': 18,
                  'gpio': 1}

for ec_index, ec_config in configuration_dictionary.items():
    if ec_index not in CAVITY_INDEXES:
        raise Exception('unknown index {}'.format(ec_index))
    if set(config_example.keys()) != set(ec_config.keys()):
        raise Exception('some required configuration keys are missing, or more than required have been provided')
    if set(config_example['s2params'].keys()) != set(ec_config['s2params'].keys()):
        raise Exception('some s2params required configuration keys are missing, or more than required have been provided')


logger.info('loaded configuration: {}'.format(configuration_dictionary))


WL_INCREMENT = 3.0

EXCLUDED_WL_RANGE = [1450, 1750]


def get_scanning_wavelengths(wl_step=WL_INCREMENT):
    intervals = [configuration_dictionary[CAVITY1_INDEX]['wavelength'],
                 configuration_dictionary[CAVITY2_INDEX]['wavelength'],
                 configuration_dictionary[CAVITY3_INDEX]['wavelength'],
                 configuration_dictionary[CAVITY4_INDEX]['wavelength']]
    min_wl = min(x[0] for x in intervals)
    max_wl = max(x[1] for x in intervals)
    return [x for x in numpy.arange(min_wl, max_wl, wl_step).tolist()
            if (x < EXCLUDED_WL_RANGE[0] or x > EXCLUDED_WL_RANGE[1])]


if __name__ == '__main__':
    print(get_scanning_wavelengths())
