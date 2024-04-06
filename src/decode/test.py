def text_to_custom_symbols(text):
    binary_text = " ".join(format(ord(char), "08b") for char in text)
    binary_text += " " + "01111100"
    return binary_text.split()


encoded_header = text_to_custom_symbols("text/plain:52")
print(" ".join(encoded_header))

"""
['11011110', '11001111', '11010010', '11011110', '10000101', '11011010', '11000110', '11001011', '11000011', '11000100', '10010000', '10011111', '10011000', '11010110', '11100010', '11001111', '11000110', '11000110', '11000101', '10000110', '10001010', '11111101', '11000101', '11011000', '11000110', '11001110', '10001011']

110111101100111111010010110111101000010111011010110001101100101111000011110001001001000010011111100110001101011011100010110011111100011011000110110001011000011010001010111111011100010111011000110001101100111010001011




var t on generate and decode match
[0.00000000e+00 2.08333333e-05 4.16666667e-05 ... 6.39375000e-02 6.39583333e-02 6.39791667e-02]

[0.00000000e+00 2.08333333e-05 4.16666667e-05 ... 6.39375000e-02 6.39583333e-02 6.39791667e-02]






[0.00000000e+00 2.61799388e-02 5.23598776e-02 ... 8.03462321e+01
 8.03724121e+01 8.03985920e+01]

"""