import base64
import multiprocessing
import sys

import colorama
import numpy as np
from colorama import Style

from . import printing

colorama.init(autoreset=True)


def text_to_mfsk(text):
    binary_text = "".join(format(ord(char), "08b") for char in text)
    return [binary_text[i : i + 2] for i in range(0, len(binary_text), 2)]


def mfsk_to_text(symbols):
    binary_text = "".join(symbols)
    chars = [binary_text[i : i + 8] for i in range(0, len(binary_text), 8)]
    return "".join(chr(int(char, 2)) for char in chars)


class Generator:
    def __init__(self, data, symbol_map, symbol_rate, fs, data_type):
        self.data = data
        self.symbol_map = symbol_map
        self.symbol_rate = symbol_rate
        self.fs = fs
        self.data_type = data_type

    def generate_signal_chunk(
        self, chunk_start, chunk_end, mfsk_data, symbol_map, symbol_rate, fs
    ) -> np.ndarray[np.int16]:
        chunk_signal = np.array([], dtype=np.int16)
        for idx in range(chunk_start, chunk_end):
            symbol = mfsk_data[idx]
            frequency = symbol_map[symbol]
            t = np.arange(0, 1 / symbol_rate, 1 / fs)
            phase = 2 * np.pi * frequency * t
            carrier = np.sin(phase)
            chunk_signal = np.append(chunk_signal, (carrier * 32767).astype(np.int16))
        return chunk_signal

    def generate_mfsk_signal(self) -> np.ndarray[np.int16]:
        printing.message(
            f"\nPreparing signal generation for data of type `{self.data_type}`..."
        )
        signal = np.array([], dtype=np.int16)

        combined_data = f"{self.data_type}:{len(self.data)}:"
        try:
            full_data = (
                f"{combined_data}{base64.b64encode(self.data.encode()).decode()}"
            )
        except AttributeError:
            full_data = f"{combined_data}{base64.b64encode(self.data).decode()}"

        printing.message(f"Turning data into symbols...")
        mfsk_data = text_to_mfsk(full_data)

        printing.message(f"Generating signal...\n")
        num_symbols = len(mfsk_data)
        num_cores = max(
            1, multiprocessing.cpu_count() // 2
        )  # Use half of available cores
        chunk_size = num_symbols // num_cores
        chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_cores - 1)]
        chunks.append((chunks[-1][1], num_symbols))

        progress = 0

        with multiprocessing.Pool(processes=num_cores) as pool:
            for chunk_start, chunk_end in chunks:
                chunk_signal = pool.apply(
                    self.generate_signal_chunk,
                    args=(
                        chunk_start,
                        chunk_end,
                        mfsk_data,
                        self.symbol_map,
                        self.symbol_rate,
                        self.fs,
                    ),
                )
                signal = np.append(signal, chunk_signal)
                progress += chunk_end - chunk_start
                print(
                    f"\r{Style.BRIGHT}Progress....:{Style.RESET_ALL} {progress}/{num_symbols} ({progress/num_symbols:.2%})",
                    end="",
                )

        if not mfsk_to_text(mfsk_data) == full_data:
            printing.notice(
                "ERROR", "Couldn't generate a signal to match to the provided data!"
            )
            sys.exit(1)

        print()
        return signal


class Demodulate:
    def __init__(self, signal: np.ndarray[np.int16], symbol_map: dict, symbol_rate: int, fs: int) -> None:
        self.signal = signal
        self.symbol_map = symbol_map
        self.symbol_rate = symbol_rate
        self.fs = fs
    
    # For any future updates
    
    def demodulate_mfsk_signal(self) -> list:
        symbol_duration = int(self.fs / self.symbol_rate)
        symbols = []
        for i in range(0, len(self.signal), symbol_duration):
            symbol_signal = self.signal[i:i + symbol_duration]

            # Freq detection
            frequencies = np.fft.fft(symbol_signal)
            freq_index = np.argmax(np.abs(frequencies[1:len(frequencies)//2])) + 1
            frequency = freq_index * self.fs / len(frequencies)

            # Map freq to symbol
            symbol = None
            for key, value in self.symbol_map.items():
                if abs(value - frequency) < 100:
                    symbol = key
                    break
            if symbol is None:
                continue
            
            symbols.append(symbol)
        
        return symbols
        