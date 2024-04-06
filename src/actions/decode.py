import base64
import glob
import wave
from os import path
from sys import exit

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from colorama import Fore, Style

import constants
import helpers.printing as printing
import helpers.signal as hsignal


def start() -> None:
    signals_dir = path.abspath(constants.SIGNALS_DIR)
    
    file_paths = glob.glob(path.join(signals_dir, constants.FILE_FORMAT))
    file_paths.sort(reverse=True)
    
    files = []
    print(
        f"{Style.BRIGHT}Which file do you want to decode?{Style.RESET_ALL} {Fore.MAGENTA}(Top is most recent){Style.RESET_ALL}"
    )
    for idx, file_path in enumerate(file_paths):
        file_name = path.basename(file_path)
        print(f" {Style.BRIGHT}{idx}.{Style.RESET_ALL} {file_name}")
        files.append((idx, file_path, file_name))
    
    file_number = printing.prompt("File Number")
    
    try:
        file_number = int(file_number)
    except ValueError:
        printing.notice("ERROR", "You must input an integer!")
        exit(1)

    if file_number < 0 or file_number > len(files) - 1:
        printing.notice("ERROR", f"File number {file_number} does not exist!")
        exit(1)

    signal_file = files[file_number]
    printing.notice("Demodulating and Decoding File", f"{signal_file[2]}...")
    
    with wave.open(signal_file[1], "rb") as wf:
        num_frames = wf.getnframes()
        frames = wf.readframes(num_frames)

        # Convert frames to numpy array of 16-bit integers
        signal = np.frombuffer(frames, dtype=np.int16)

    sd.play(signal, constants.FS, blocking=False)
    printing.notice("Signal", signal)
    
    demodulator = hsignal.Demodulate(signal, constants.SYMBOL_MAP, constants.SYMBOL_RATE, constants.FS)
    data = demodulator.demodulate_mfsk_signal()
    printing.notice("Data", data)

    data_decoded = hsignal.mfsk_to_text(data)
    printing.notice("Data Decoded", data_decoded)
    data_decoded = data_decoded.split(":")
    printing.notice("Data Type", data_decoded[0])
    printing.notice("Data Length", data_decoded[1])
    try:
        printing.notice("Data Contents", f"\n {base64.b64decode(data_decoded[2]).decode()}")
    except UnicodeDecodeError: # bytes/whatever tf
        printing.notice("Data Contents", f"\n {base64.b64decode(data_decoded[2])}")

    show_plot = printing.prompt("Do you want to show the frequency plot (laggy for larger signals)? [y/N]")
    if show_plot.lower() in ["y", "yes"]:
        plt.plot(signal)
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.title("Loaded WAV File Signal")
        plt.show()
    
    printing.message("\nPress any key to exit...")
    input()        
    return