import base64

import numpy as np
import sounddevice as sd

MODULATION = { 
    '000' : (0.5,   0),
    '001' : (0.5,  90),
    '010' : (0.5, 180),
    '011' : (0.5, 270),
    '100' : (1.0,   0),
    '101' : (1.0,  90),
    '110' : (1.0, 180),
    '111' : (1.0, 270),
}
BAUD_RATE = 10
BITS_PER_BAUS = 3
CARRIER_FREQ = 50
