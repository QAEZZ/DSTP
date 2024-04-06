import time
import wave
from os import path
from sys import exit

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from colorama import Fore, Style

import constants
import helpers.printing as printing
import helpers.signal as hsignal


def start() -> None:
    print(f"{Style.BRIGHT}What is the data type that you're sending?")
    for idx, data_type in enumerate(constants.GENERATE_DATA_TYPES):
        print(f" {Style.BRIGHT}{idx}.{Style.RESET_ALL} {data_type}")

    data_type = printing.prompt("Data Type")
    try:
        data_type = int(data_type)
    except ValueError:
        printing.notice("ERROR", "You must input an integer!")
        exit(1)

    if data_type < 0 or data_type > len(constants.GENERATE_DATA_TYPES) - 1:
        printing.notice("ERROR", f"Data type {data_type} does not exist!")
        exit(1)

    data_type = constants.GENERATE_DATA_TYPES[data_type]

    match data_type.lower():
        case "text":
            is_file_upload = printing.prompt("Do you want to upload a file? [y/N]")
            if is_file_upload.lower() in ["y", "yes"]:
                file_path = printing.prompt("Please paste the file path")
                if not path.exists(file_path) or not path.isfile(file_path):
                    printing.notice("ERROR", "The path does not exist or isn't a file!")
                    exit(1)

                with open(file_path, "r") as f:
                    data = f.read()
            else:
                is_file_upload = True
                print(f"{Style.BRIGHT}Please type your text below:")
                data = input()
        case "png" | "jpg":
            file_path = printing.prompt("Please paste the file path")
            if not path.exists(file_path) or not path.isfile(file_path):
                printing.notice("ERROR", "The path does not exist or isn't a file!")
                exit(1)

            with open(file_path, "rb") as f:
                data = f.read()
        case _:
            data = "No data."

    generator = hsignal.Generator(data, constants.SYMBOL_MAP, constants.SYMBOL_RATE, constants.FS, data_type)
    signal = generator.generate_mfsk_signal()

    printing.notice("Signal......", signal)

    sd.play(signal, constants.FS)
    printing.notice("Signal DType", signal.dtype)

    cur_time = time.time()
    printing.message(
        f"\nSaving to `{path.abspath(f'{constants.SIGNALS_DIR}/drpfd-{constants.FS}-{constants.SYMBOL_RATE}-{int(cur_time)}.wav')}`..."
    )
    sf.write(
        path.abspath(
            f"{constants.SIGNALS_DIR}/drpfd-{constants.FS}-{constants.SYMBOL_RATE}-{int(cur_time)}.wav"
        ),
        signal,
        constants.FS,
    )

    printing.message("Checking WAV file integrity...\n")

    with wave.open(
        path.abspath(
            f"{constants.SIGNALS_DIR}/drpfd-{constants.FS}-{constants.SYMBOL_RATE}-{int(cur_time)}.wav"
        ),
        "rb",
    ) as wf:
        num_frames = wf.getnframes()
        frames = wf.readframes(num_frames)

        # Convert frames to numpy array of 16-bit integers
        read_signal = np.frombuffer(frames, dtype=np.int16)

    printing.notice("File Signal.", read_signal)
    signal_integrity = np.subtract(signal, read_signal)
    is_all_zeros = np.all(signal_integrity == 0)
    printing.notice(
        "Integrity...",
        (
            f"{Fore.GREEN}PASS"
            if is_all_zeros
            else f"{Fore.RED}FAIL, the signal generated does not match the signal in the WAV file."
        ),
    )

    show_plot = printing.prompt(
        "Do you want to show the frequency plot (laggy for larger signals)? [y/N]"
    )
    if show_plot.lower() in ["y", "yes"]:
        plt.plot(signal)
        plt.title("Signal")
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.show()

    printing.message("\nPress any key to quit...")
    input()
    return
