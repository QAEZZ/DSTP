FS = 48000  # Sampling frequency (Hz)
SYMBOL_RATE = 100  # baud
FREQUENCIES = [400, 800, 1200, 1600]  # Frequencies for MFSK
SYMBOL_MAP = {
    "00": FREQUENCIES[0],
    "01": FREQUENCIES[1],
    "10": FREQUENCIES[2],
    "11": FREQUENCIES[3],
}  # Symbol-to-frequency mapping

SIGNALS_DIR = "./signals"
FILE_FORMAT = "drpfd-*-*-*.wav"

GENERATE_DATA_TYPES = ["text", "png", "jpg"]