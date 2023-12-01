import json

CAVITY1_INDEX = 'ec1'
CAVITY2_INDEX = 'ec2'
CAVITY3_INDEX = 'ec3'
CAVITY4_INDEX = 'ec4'
CAVITY1_URL = 'http://0.0.0.0:5001/ec/api/v1.0'
CAVITY2_URL = 'http://0.0.0.0:5002/ec/api/v1.0'
CAVITY3_URL = 'http://0.0.0.0:5003/ec/api/v1.0'
CAVITY4_URL = 'http://0.0.0.0:5004/ec/api/v1.0'

ADC_CHANNEL = 0
REF = 5.08  # Modify according to actual voltage (read voltage) external AVDD and AVSS (Default), or internal 2.5V
configuration_dictionary = {
    CAVITY1_INDEX: {'wavelength': [1037.2, 1353.6], 'x_position': -18.65, 'y_position': 0.5,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 18.6,
                                 'out_width': 3}, 'temperature_setpoint': 18,
                    'gpio': 1},
    CAVITY2_INDEX: {'wavelength': [846.0, 1037.1], 'x_position': -16.75, 'y_position': -0.65,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 19.3,
                                 'out_width': 4}, 'temperature_setpoint': 18,
                    'gpio': 2},
    CAVITY3_INDEX: {'wavelength': [1600.8, 1813.9], 'x_position': -14.35, 'y_position': -0.1,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 15.4,  'out_width': 4}, 'temperature_setpoint': 18,
                    'gpio': 3},
    CAVITY4_INDEX: {'wavelength': [1354, 1600], 'x_position': -5.5, 'y_position': -1.5,
                    's2params': {'pulse_period': 6000, 'pulse_width': 300,
                                 'pulsing_mode': 'internal', 'applied_voltage': 17.2,  'out_width': 4}, 'temperature_setpoint': 18,
                    'gpio': 3}
}

with open('/home/samuele/phoot.json', 'w') as f:
    json.dump(configuration_dictionary, f)