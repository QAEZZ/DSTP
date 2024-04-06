import sounddevice as sd
import soundfile as sf
from os import path
import helpers
import time
import wave
import numpy as np
from colorama import Style, Fore
from sys import exit

fs = 48000  # Sampling frequency (Hz)
symbol_rate = 100  # baud
frequencies = [400, 800, 1200, 1600]  # Frequencies for MFSK
symbol_map = {
    "00": frequencies[0],
    "01": frequencies[1],
    "10": frequencies[2],
    "11": frequencies[3],
}  # Symbol-to-frequency mapping


if __name__ == "__main__":
    data_types = ["text", "png", "jpg"]
    print(f"{Style.BRIGHT}What is the data type that you're sending?")
    for idx, data_type in enumerate(data_types):
        print(f" {Style.BRIGHT}{idx}.{Style.RESET_ALL} {data_type}")

    data_type = helpers.prompt("Data Type")
    try:
        data_type = int(data_type)
    except ValueError:
        helpers.notice("ERROR", "You must input an integer!")
        exit(1)

    if data_type < 0 or data_type > len(data_types) - 1:
        helpers.notice("ERROR", f"Data type {data_type} does not exist!")
        exit(1)

    data_type = data_types[data_type]

    match data_type.lower():
        case "text":
            is_file_upload = helpers.prompt("Do you want to upload a file? [y/N]")
            if is_file_upload.lower() in ["y", "yes"]:
                file_path = helpers.prompt("Please paste the file path")
                if not path.exists(file_path) or not path.isfile(file_path):
                    helpers.notice("ERROR", "The path does not exist or isn't a file!")
                    exit(1)

                with open(file_path, "r") as f:
                    data = f.read()
            else:
                is_file_upload = True
                print(f"{Style.BRIGHT}Please type your text below:")
                data = input()
        case "png" | "jpg":
            file_path = helpers.prompt("Please paste the file path")
            if not path.exists(file_path) or not path.isfile(file_path):
                helpers.notice("ERROR", "The path does not exist or isn't a file!")
                exit(1)

            with open(file_path, "rb") as f:
                data = f.read()
        case _:
            data = "No data."

    signal = helpers.generate_mfsk_signal(data, symbol_map, symbol_rate, fs, data_type)

    helpers.notice("Signal......", signal)

    sd.play(signal, fs)
    helpers.notice("Signal DType", signal.dtype)

    cur_time = time.time()
    helpers.message(
        f"\nSaving to `{path.abspath(f'../signals/drpfd-{fs}-{symbol_rate}-{int(cur_time)}.wav')}`..."
    )
    sf.write(path.abspath(f"../signals/drpfd-{fs}-{symbol_rate}-{int(cur_time)}.wav"), signal, fs)

    helpers.message("Checking WAV file integrity...\n")

    with wave.open(
        path.abspath(f"../signals/drpfd-{fs}-{symbol_rate}-{int(cur_time)}.wav"), "rb"
    ) as wf:
        num_frames = wf.getnframes()
        frames = wf.readframes(num_frames)

        # Convert frames to numpy array of 16-bit integers
        read_signal = np.frombuffer(frames, dtype=np.int16)

    helpers.notice("File Signal.", read_signal)
    signal_integrity = np.subtract(signal, read_signal)
    is_all_zeros = np.all(signal_integrity == 0)
    helpers.notice(
        "Integrity...",
        (
            f"{Fore.GREEN}PASS"
            if is_all_zeros
            else f"{Fore.RED}FAIL, the signal generated does not match the signal in the WAV file."
        ),
    )

    input("\nPress any key to quit...")
