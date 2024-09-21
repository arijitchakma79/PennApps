import numpy as np
import noisereduce as nr
import sounddevice as sd
import soundfile as sf
from scipy.signal import butter, lfilter
import collections  # To handle the moving average

class NoiseReduction:
    def __init__(self, lowcut, highcut, threshold, sr, reduction_score):
        self.lowcut = lowcut
        self.highcut = highcut
        self.threshold = threshold
        self.sr = sr
        self.reduction_score = reduction_score
        self.previous_rms = collections.deque(maxlen=10)  # Store the last 10 RMS values

    def butter_bandpass(self, fs, order=5):
        nyquist = 0.5 * fs
        low = self.lowcut / nyquist
        high = self.highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, fs, order=10):
        b, a = self.butter_bandpass(fs, order=order)
        y = lfilter(b, a, data)
        return y

    def calculate_moving_average(self):
        if len(self.previous_rms) == 0:
            return 0
        return np.mean(self.previous_rms)

    def process_chunk(self, chunk):
        # Calculate the RMS amplitude of the current chunk
        rms_amplitude = np.sqrt(np.mean(np.square(chunk)))
        print(f"RMS Amplitude: {rms_amplitude}")

        # Calculate the moving average of the last 10 amplitudes
        moving_average = self.calculate_moving_average()
        print(f"Moving Average of last 10 RMS values: {moving_average}")

        # Detect sudden changes compared to the moving average
        if abs(rms_amplitude - moving_average) > self.threshold:
            print("Sudden noise detected, but no action is taken (as requested).")
            # You can trigger any action here if needed

        # Store the current RMS amplitude in the history
        self.previous_rms.append(rms_amplitude)

        # Skip processing if the amplitude is below the threshold
        if rms_amplitude < self.threshold:
            print("Amplitude below threshold, skipping processing.")
            return chunk

        print("Amplitude above threshold, processing audio...")

        # Apply the bandpass filter to isolate speech frequencies
        filtered_chunk = self.bandpass_filter(chunk, self.sr)

        # Apply noise reduction to the chunk
        reduced_noise_chunk = nr.reduce_noise(y=filtered_chunk, sr=self.sr, prop_decrease=0.95)

        # Mix the original and reduced audio based on the reduction score
        final_chunk = (1 - self.reduction_score) * filtered_chunk + self.reduction_score * reduced_noise_chunk

        return final_chunk