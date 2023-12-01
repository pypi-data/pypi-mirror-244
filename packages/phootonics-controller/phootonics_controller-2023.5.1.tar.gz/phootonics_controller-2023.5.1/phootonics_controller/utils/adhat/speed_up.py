

import timeit

from phootonics_controller.base_controllers.main_controller import ADCDevice

if __name__ == '__main__':
    adc = ADCDevice()
    adc.initialise()
    number = 1000
    print(timeit.timeit('adc.read_fast()', globals=globals(),
                        number=number)/number)

