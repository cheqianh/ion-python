from io import FileIO

from amazon.ion.simpleion import dump

import ctypes as _ctypes

if __name__ == '__main__':
    adder = _ctypes.cdll.LoadLibrary('/Users/cheqianh/Desktop/ion-python/ionc')

    sum = adder.add_int(3, 4)
    print(sum)


