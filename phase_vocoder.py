import numpy as np
import scipy.signal
import scipy.io.wavfile
import argparse


def phase_vocoder(input_signal, rate_change):
    # Params
    fft_size = 2048
    hop_size = fft_size // 4

    #window = scipy.signal.windows.hann(fft_size)
    window = scipy.signal.windows.kaiser(fft_size, beta=3)

    input_signal = np.concatenate((np.zeros(fft_size), input_signal, np.zeros(fft_size)))
    output_signal = np.zeros(int(len(input_signal) / rate_change) + fft_size)

    output_index = 0
    for i in range(0, len(input_signal) - fft_size, hop_size):
        frame = input_signal[i:i+fft_size] * window

        spectrum = np.fft.fft(frame)

        phase_accumulator = np.angle(spectrum)
    
        adjusted_spectrum = np.abs(spectrum) * np.exp(1j * phase_accumulator * rate_change)

        output_frame = np.fft.ifft(adjusted_spectrum).real

        output_index_start = int(i / rate_change)
        output_index_end = int(i / rate_change + fft_size)
        output_signal[output_index_start:output_index_end] += output_frame * window
        output_index = output_index_end

    output_signal = output_signal[:output_index]

    return output_signal[fft_size // 2:-fft_size // 2]

def run_script(input_path, output_path, time_stretch_ratio):

    time_stretch_ratio = float(time_stretch_ratio)
    print(input_path, output_path, time_stretch_ratio, type(time_stretch_ratio))

    sample_rate, input_signal = scipy.io.wavfile.read(input_path)
    input_signal = input_signal.astype(float) / 32767.0 # Normalize

    # stretched_signal = phase_vocoder(input_signal, 2)

    # compressed_signal = phase_vocoder(input_signal, 0.5)

    converted_signal = phase_vocoder(input_signal, time_stretch_ratio)

    #scipy.io.wavfile.write("test_mono_r2.wav", sample_rate, (stretched_signal * 32767).astype(np.int16))
    #scipy.io.wavfile.write("test_mono_r05.wav", sample_rate, (compressed_signal * 32767).astype(np.int16))
    scipy.io.wavfile.write(output_path, sample_rate, (converted_signal * 32767).astype(np.int16))
    print('The script execution was completed successfully.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="algorithm")
    parser.add_argument('input', help='input_path')
    parser.add_argument('output', help='output_path')
    parser.add_argument('time_stretch_ratio', help='time_stretch_ratio')
    args = parser.parse_args()

    run_script(args.input, args.output, args.time_stretch_ratio)


