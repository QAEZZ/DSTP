import matplotlib.pyplot as plt


def show_plot(signal):
    plt.plot(signal)
    plt.title("mfsk Signal")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.show()