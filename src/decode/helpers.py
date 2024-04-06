import colorama
from colorama import Fore, Style
import numpy as np

colorama.init(autoreset=True)

def notice(header: str, notice: str) -> None:
    print(f"{Style.BRIGHT}{header}:{Style.RESET_ALL} {notice}")

def prompt(to_prompt: str) -> str:
    return input(f"{Style.BRIGHT}{to_prompt}:{Style.RESET_ALL} ")

# def mfsk_to_text(mfsk):
#     frequencies = [
#         100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600
#     ]
#     symbol_map = {  # Symbol-to-frequency mapping
#         "0000": frequencies[0],
#         "0001": frequencies[1],
#         "0010": frequencies[2],
#         "0011": frequencies[3],
#         "0100": frequencies[4],
#         "0101": frequencies[5],
#         "0110": frequencies[6],
#         "0111": frequencies[7],
#         "1000": frequencies[8],
#         "1001": frequencies[9],
#         "1010": frequencies[10],
#         "1011": frequencies[11],
#         "1100": frequencies[12],
#         "1101": frequencies[13],
#         "1110": frequencies[14],
#         "1111": frequencies[15],
#     }

#     binary_text = "".join([format(frequencies.index(int(symbol_map[symbol])), "04b") for symbol in mfsk])
#     text = "".join([chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)])
#     return text

# def mfsk_signal_to_text(signal):
#     frequencies = [
#         100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600
#     ]
#     symbol_map = {  # Symbol-to-frequency mapping
#         "0000": frequencies[0],
#         "0001": frequencies[1],
#         "0010": frequencies[2],
#         "0011": frequencies[3],
#         "0100": frequencies[4],
#         "0101": frequencies[5],
#         "0110": frequencies[6],
#         "0111": frequencies[7],
#         "1000": frequencies[8],
#         "1001": frequencies[9],
#         "1010": frequencies[10],
#         "1011": frequencies[11],
#         "1100": frequencies[12],
#         "1101": frequencies[13],
#         "1110": frequencies[14],
#         "1111": frequencies[15],
#     }

#     # Split signal into chunks of 4 samples each
#     chunks = [signal[i:i+4] for i in range(0, len(signal), 4)]

#     # Calculate average magnitude of each chunk
#     avg_magnitudes = [np.mean(np.abs(chunk)) for chunk in chunks]

#     # Determine the frequency for each chunk
#     frequencies = [int(round(avg * 1600)) for avg in avg_magnitudes]

#     # Map frequency to symbol
#     symbols = [format(frequencies.index(freq), "04b") for freq in frequencies]

#     # Convert symbols to binary text
#     binary_text = "".join(symbols)

#     # Convert binary text to text
#     text = "".join([chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)])

#     return text

# def mfsk_signal_to_text(signal, frequencies, symbol_map, symbol_rate, fs):
#     count = 0
#     for symbol in signal:
#         if count > 10: break
#         print(symbol)
#         count += 1

def mfsk_to_text(symbols):
    binary_text = "".join(symbols)
    chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    return "".join(chr(int(char, 2)) for char in chars)


def demodulate_mfsk_signal(signal, symbol_map, symbol_rate, fs):
    symbol_duration = int(fs / symbol_rate)
    symbols = []
    for i in range(0, len(signal), symbol_duration):
        symbol_signal = signal[i:i + symbol_duration]

        # Perform frequency detection
        frequencies = np.fft.fft(symbol_signal)
        freq_index = np.argmax(np.abs(frequencies[1:len(frequencies)//2])) + 1
        frequency = freq_index * fs / len(frequencies)

        # Map frequency to symbol
        symbol = None
        for key, value in symbol_map.items():
            if abs(value - frequency) < 100:  # Adjust the threshold as needed
                symbol = key
                break
        if symbol is None:
            continue

        symbols.append(symbol)

    return symbols





# def demodulate_mfsk_signal(signal, symbol_map, symbol_rate, fs) -> tuple[str, int, str]:
#     header_symbols = []
#     data_symbols = []
#     end_of_header_sequence = "01111100"
#     past_symbols = ["", "", ""]
#     still_demodulating_header = True

#     # Perform symbol synchronization and demodulation
#     for i in range(0, len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]
        
#         symbol_phase_diffs = []
#         for symbol, freq in symbol_map.items():
#             carrier = np.sin(2 * np.pi * freq * t)
#             phase_diff = np.angle(np.sum(segment * carrier)) % (2 * np.pi)
#             symbol_phase_diffs.append((symbol, phase_diff))

#         symbol_phase_diffs.sort(key=lambda x: x[1])
#         symbol = symbol_phase_diffs[0][0]

#         # Check for end of header sequence
#         if "".join(past_symbols[-3:]) == end_of_header_sequence:
#             print("end of header")
#             break  # End of header

#         past_symbols.append(symbol)
#         header_symbols.append(symbol)
#         past_symbols.pop(0)


#     # Decode header
#     notice("Header Symbols", header_symbols)

#     header_data = "".join(header_symbols)
#     notice("Header Data", header_data)


#     # Split header binary into bytes and convert to ASCII chars
#     header_data = header_data.replace(" ", "") 
#     header_data_bytes = [header_data[i:i + 8] for i in range(0, len(header_data), 8)]
#     notice("Header Data Bytes", header_data_bytes)
#     header_ascii = "".join([chr(int(byte, 2)) for byte in header_data_bytes])
#     notice("Header ASCII Data", header_ascii)

#     mime_type, data_length = header_ascii.split(":")

#     # Decode data symbols
#     data_length = int(data_length)
#     for i in range(len(header_symbols) * int(fs / symbol_rate), len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]
#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]
#         if symbol == "00":
#             break  # End of data symbols

#         data_symbols.append(symbol)

#     # Decode data
#     data = mfsk_to_text(data_symbols)

#     return mime_type, data_length, data


# def demodulate_mfsk_signal(signal, symbol_map, symbol_rate, fs):
#     header_symbols = []
#     data_symbols = []
#     end_of_header_sequence = "01111100"
#     past_symbols = ["", "", ""]

#     # Perform symbol synchronization and demodulation
#     for i in range(0, len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]

#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]

#         # Check for end of header sequence
#         if "".join(past_symbols[-3:]) == end_of_header_sequence:
#             break  # End of header

#         past_symbols.append(symbol)
#         header_symbols.append(symbol)
#         past_symbols.pop(0)

#     # Decode header
#     notice("Header Symbols", header_symbols)
#     header_binary = "".join(header_symbols)
#     notice("Header Binary", header_binary)

#     # Split header binary into bytes and convert to ASCII characters
#     header_data = ""
#     for i in range(0, len(header_binary), 8):
#         byte = header_binary[i:i + 8]
#         if len(byte) == 8:
#             header_data += chr(int(byte, 2))

#     notice("Header Data", header_data)

#     mime_type, data_length = header_data.split(":")

#     # Decode data symbols
#     data_length = int(data_length)
#     for i in range(len(header_symbols) * int(fs / symbol_rate), len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]
#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]
#         if symbol == "00":
#             break  # End of data symbols

#         data_symbols.append(symbol)

#     # Decode data
#     data = mfsk_to_text(data_symbols)

#     return mime_type, data_length, data


# def demodulate_mfsk_signal(signal, symbol_map, symbol_rate, fs):
#     header_symbols = []
#     data_symbols = []
#     end_of_header_sequence = "01111100"
#     past_symbols = ["", "", ""]

#     # Perform symbol synchronization and demodulation
#     for i in range(0, len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]

#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]

#         # Check for end of header sequence
#         if "".join(past_symbols[-3:]) == end_of_header_sequence:
#             break  # End of header

#         past_symbols.append(symbol)
#         header_symbols.append(symbol)
#         past_symbols.pop(0)

#     # Decode header
#     notice("Header Symbols", header_symbols)
#     # header_data = " ".join(header_symbols)  # Convert list of symbols to binary string
#     header_data = "".join(header_symbols)

#     # Add a space every 8 characters
#     header_data_spaced = ""
#     for i, char in enumerate(header_data):
#         header_data_spaced += char
#         if (i + 1) % 8 == 0 and i != len(header_data) - 1:
#             header_data_spaced += " "  # Add a space every 8 characters, except at the end
#     notice("Header Data", header_data_spaced)


#     mime_type, data_length = header_data.split(":")

#     # Decode data symbols
#     data_length = int(data_length)
#     for i in range(len(header_symbols) * int(fs / symbol_rate), len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]
#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]
#         if symbol == "00":
#             break  # End of data symbols

#         data_symbols.append(symbol)

#     # Decode data
#     data = mfsk_to_text(data_symbols)

#     return mime_type, data_length, data




# def demodulate_mfsk_signal(signal, symbol_map, symbol_rate, fs):
#     pilot_freq = 2000
#     pilot_dur = 0.5
#     pilot_samples = int(fs * pilot_dur)
#     header_symbols = []
#     data_symbols = []

#     # Perform carrier recovery, symbol synchronization, and demodulation
#     for i in range(pilot_samples, len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]
#         # correlation = np.abs(np.correlate(segment, np.sin(2 * np.pi * pilot_freq * t)))[0]
#         # print(correlation)
#         # if correlation > 0.9 * len(t):
#         #     print("skipping pilot tone")
#         #     continue  # Skip pilot tone

#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             print(symbol, freq)
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]
#         if symbol == "00":
#             break  # End of header symbols

#         header_symbols.append(symbol)

#     # Decode header
#     notice("Header Symbols", header_symbols)
#     header_data = mfsk_to_text(header_symbols)
#     notice("Header Data", header_data)
#     mime_type, data_length = header_data.split(":")

#     # Decode data symbols
#     data_length = int(data_length)
#     for i in range(len(header_symbols) * int(fs / symbol_rate), len(signal), int(fs / symbol_rate)):
#         t = np.arange(0, 1 / symbol_rate, 1 / fs)
#         segment = signal[i:i + len(t)]
#         symbol_freq = []
#         for symbol, freq in symbol_map.items():
#             phase_diff = np.angle(np.sum(segment * np.exp(-1j * 2 * np.pi * freq * t))) % (2 * np.pi)
#             symbol_freq.append((symbol, phase_diff))

#         symbol_freq.sort(key=lambda x: x[1])
#         symbol = symbol_freq[0][0]
#         if symbol == "00":
#             break  # End of data symbols

#         data_symbols.append(symbol)

#     # Decode data
#     data = mfsk_to_text(data_symbols)

#     return mime_type, data_length, data
    