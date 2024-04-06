import base64
import glob
import wave
from os import path
from sys import exit

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from colorama import Fore, Style

import helpers

fs = 48000  # Sampling frequency (Hz)
symbol_rate = 100  # baud
frequencies = [400, 800, 1200, 1600]  # Frequencies for MFSK
symbol_map = {
    "00": frequencies[0],
    "01": frequencies[1],
    "10": frequencies[2],
    "11": frequencies[3],
}  # Symbol-to-frequency mapping
# frequencies = [
#     100,
#     200,
#     300,
#     400,
#     500,
#     600,
#     700,
#     800,
#     900,
#     1000,
#     1100,
#     1200,
#     1300,
#     1400,
#     1500,
#     1600,
# ]
# symbol_map = {  # Symbol-to-frequency mapping
#     "0000": frequencies[0],
#     "0001": frequencies[1],
#     "0010": frequencies[2],
#     "0011": frequencies[3],
#     "0100": frequencies[4],
#     "0101": frequencies[5],
#     "0110": frequencies[6],
#     "0111": frequencies[7],
#     "1000": frequencies[8],
#     "1001": frequencies[9],
#     "1010": frequencies[10],
#     "1011": frequencies[11],
#     "1100": frequencies[12],
#     "1101": frequencies[13],
#     "1110": frequencies[14],
#     "1111": frequencies[15],
# }

if __name__ == "__main__":
    signals_dir = path.abspath("../signals")

    file_paths = glob.glob(path.join(signals_dir, "drpfd-*-*-*.wav"))
    file_paths.sort(reverse=True)

    files = []
    print(
        f"{Style.BRIGHT}Which file do you want to decode?{Style.RESET_ALL} {Fore.MAGENTA}(Top is most recent){Style.RESET_ALL}"
    )
    for idx, file_path in enumerate(file_paths):
        file_name = path.basename(file_path)
        print(f" {Style.BRIGHT}{idx}.{Style.RESET_ALL} {file_name}")
        files.append((idx, file_path, file_name))

    # file_number = input(f"{Style.BRIGHT}File Number: {Style.RESET_ALL}")
    file_number = helpers.prompt("File Number")

    try:
        file_number = int(file_number)
    except ValueError:
        helpers.notice("ERROR", "You must input an integer!")
        exit(1)

    if file_number < 0 or file_number > len(files) - 1:
        helpers.notice("ERROR", f"File number {file_number} does not exist!")
        exit(1)

    signal_file = files[file_number]
    helpers.notice("Decoding File", f"{signal_file[2]}...")

    with wave.open(signal_file[1], "rb") as wf:
        num_frames = wf.getnframes()
        frames = wf.readframes(num_frames)

        # Convert frames to numpy array of 16-bit integers
        signal = np.frombuffer(frames, dtype=np.int16)

    sd.play(signal, fs, blocking=False)
    helpers.notice("Signal", signal)

    # data = helpers.demodulate_mfsk_signal(
    #     signal, frequencies, symbol_map, symbol_rate, fs
    # )
    # print(data)
    data = helpers.demodulate_mfsk_signal(signal, symbol_map, symbol_rate, fs)
    helpers.notice("Data", data)

    data_decoded = helpers.mfsk_to_text(data)
    helpers.notice("Data Decoded", data_decoded)
    data_decoded = data_decoded.split(":")
    helpers.notice("Data Type", data_decoded[0])
    helpers.notice("Data Length", data_decoded[1])
    try:
        helpers.notice("Data Contents", f"\n {base64.b64decode(data_decoded[2]).decode()}")
    except UnicodeDecodeError: # bytes/whatever tf
        helpers.notice("Data Contents", f"\n {base64.b64decode(data_decoded[2])}")

    input("Press any key to exit...")
    # plt.plot(signal)
    # plt.xlabel('Sample')
    # plt.ylabel('Amplitude')
    # plt.title('Loaded WAV file signal')
    # plt.show()
