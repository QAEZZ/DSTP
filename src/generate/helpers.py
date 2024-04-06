import numpy as np
import base64
import sys
import multiprocessing
from tqdm import tqdm
import colorama
from colorama import Style, Fore

colorama.init(autoreset=True)

def notice(header: str, notice: str) -> None:
    print(f"{Style.BRIGHT}{header}:{Style.RESET_ALL} {notice}")

def prompt(to_prompt: str) -> str:
    return input(f"{Style.BRIGHT}{to_prompt}:{Style.RESET_ALL} ")

def message(message: str) -> None:
    print(f"{Fore.MAGENTA}{message}")

def generate_signal_chunk(chunk_start, chunk_end, mfsk_data, symbol_map, symbol_rate, fs):
    chunk_signal = np.array([], dtype=np.int16)
    for idx in range(chunk_start, chunk_end):
        symbol = mfsk_data[idx]
        frequency = symbol_map[symbol]
        t = np.arange(0, 1 / symbol_rate, 1 / fs)
        phase = 2 * np.pi * frequency * t
        carrier = np.sin(phase)
        chunk_signal = np.append(chunk_signal, (carrier * 32767).astype(np.int16))
    return chunk_signal

def generate_mfsk_signal(data, symbol_map, symbol_rate, fs, data_type):
    message(f"\nPreparing signal generation for data of type `{data_type}`...")
    signal = np.array([], dtype=np.int16)

    is_binary = False
    combined_data = f"{data_type}:{len(data)}:"
    try:
        full_data = f"{combined_data}{base64.b64encode(data.encode()).decode()}"
    except AttributeError:
        is_binary = True
        full_data = f"{combined_data}{base64.b64encode(data).decode()}"

    message(f"Turning data into symbols...")
    mfsk_data = text_to_mfsk(full_data)

    message(f"Generating signal...\n")
    num_symbols = len(mfsk_data)
    num_cores = max(1, multiprocessing.cpu_count() // 2)  # Use half of available cores
    chunk_size = num_symbols // num_cores
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_cores - 1)]
    chunks.append((chunks[-1][1], num_symbols))

    progress = 0

    with multiprocessing.Pool(processes=num_cores) as pool:
        for chunk_start, chunk_end in chunks:
            chunk_signal = pool.apply(generate_signal_chunk, args=(chunk_start, chunk_end, mfsk_data, symbol_map, symbol_rate, fs))
            signal = np.append(signal, chunk_signal)
            progress += chunk_end - chunk_start
            print(f"\r{Style.BRIGHT}Progress....:{Style.RESET_ALL} {progress}/{num_symbols} ({progress/num_symbols:.2%})", end="")

    if not mfsk_to_text(mfsk_data) == full_data:
        notice("ERROR", "Couldn't generate a signal to match to the provided data!")
        sys.exit(1)

    print()
    return signal

# def generate_signal_chunk(chunk_start, chunk_end, mfsk_data, symbol_map, symbol_rate, fs):
#     chunk_signal = np.array([], dtype=np.int16)
#     for idx in range(chunk_start, chunk_end):
#         symbol = mfsk_data[idx]
#         frequency = symbol_map[symbol]
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         phase = 2 * np.pi * frequency * t
#         carrier = np.sin(phase)
#         chunk_signal = np.append(chunk_signal, (carrier * 32767).astype(np.int16))
#     return chunk_signal

# def generate_mfsk_signal(data, symbol_map, symbol_rate, fs, data_type):
#     message(f"\nPreparing signal generation for data of type `{data_type}`...")
#     signal = np.array([], dtype=np.int16)

#     is_bytes = False
#     combined_data = f"{data_type}:{len(data)}:"
#     try:
#         full_data = f"{combined_data}{base64.b64encode(data.encode()).decode()}"
#     except AttributeError:
#         is_bytes = True
#         full_data = f"{combined_data}{base64.b64encode(data).decode()}"

#     message(f"Turning data into symbols...")
#     mfsk_data = text_to_mfsk(full_data)

#     message(f"Generating signal...\n")
#     num_symbols = len(mfsk_data)
#     num_cores = multiprocessing.cpu_count()
#     chunk_size = num_symbols // num_cores
#     chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_cores - 1)]
#     chunks.append((chunks[-1][1], num_symbols))

#     with multiprocessing.Pool(processes=num_cores) as pool:
#         chunk_signals = pool.starmap(generate_signal_chunk, [(start, end, mfsk_data, symbol_map, symbol_rate, fs) for start, end in chunks])

#     signal = np.concatenate(chunk_signals)

#     if not mfsk_to_text(mfsk_data) == full_data:
#         notice("ERROR", "Couldn't generate a signal to match to the provided data!")
#         sys.exit(1)

#     return signal

# def generate_mfsk_signal(data, symbol_map, symbol_rate, fs, data_type):
#     message(f"\nPreparing signal generation for data of type `{data_type}`...")
#     signal = np.array([], dtype=np.int16)

#     is_bytes = False
#     combined_data = f"{data_type}:{len(data)}:"
#     try:
#         full_data = f"{combined_data}{base64.b64encode(data.encode()).decode()}"
#     except AttributeError:
#         is_bytes = True
#         full_data = f"{combined_data}{base64.b64encode(data).decode()}"

#     message(f"Turning data into symbols...")
#     mfsk_data = text_to_mfsk(full_data)

#     message(f"Generating signal...\n")
#     for idx, symbol in enumerate(mfsk_data):
#         if idx % 5:
#             message(f"{idx}/{len(mfsk_data)} ({round((idx/len(mfsk_data)), 2)}%)")
#         frequency = symbol_map[symbol]
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         phase = 2 * np.pi * frequency * t
#         carrier = np.sin(phase)

#         # Scale and convert to int16 cause wave doesnt like float64
#         signal = np.append(signal, (carrier * 32767).astype(np.int16))
    

#     if not mfsk_to_text(mfsk_data) == full_data:
#         notice("ERROR", "Couldn't generate a signal to match to the provided data!")
#         sys.exit(1)
        
#     return signal


def text_to_mfsk(text):
    binary_text = "".join(format(ord(char), "08b") for char in text)
    return [binary_text[i : i + 2] for i in range(0, len(binary_text), 2)]

def mfsk_to_text(symbols):
    binary_text = "".join(symbols)
    chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    return "".join(chr(int(char, 2)) for char in chars)