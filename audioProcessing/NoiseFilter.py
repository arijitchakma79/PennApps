import numpy as np
import noisereduce as nr
import sounddevice as sd
import soundfile as sf
from scipy.signal import butter, lfilter
import collections  


class NoiseReduction:
    def __init__(self, lowcut, highcut, threshold, sr, reduction_score, horn_lowcut=500, horn_highcut=4000):
        self.lowcut = lowcut
        self.highcut = highcut
        self.threshold = threshold
        self.sr = sr
        self.reduction_score = reduction_score  # Start with an initial reduction score
        self.previous_rms = collections.deque(maxlen=10)  # Store the last 10 RMS values
        self.horn_lowcut = horn_lowcut
        self.horn_highcut = horn_highcut
        self.loud_duration = 0  # Track how long the sound stays loud
        self.loud_threshold_duration = 3  # If sound is loud for 3 seconds (adjust as needed), reduce outside sound

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut, fs, order=10):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def calculate_moving_average(self):
        if len(self.previous_rms) == 0:
            return 0
        return np.mean(self.previous_rms)
    
    def replace_non_finite(self, audio_chunk):
        """
        Replace NaN or Inf values in the audio buffer with zeros to avoid issues during processing.
        """
        return np.nan_to_num(audio_chunk, nan=0.0, posinf=0.0, neginf=0.0)

    def process_chunk(self, chunk, chunk_duration=1.0):
        # Replace NaN or Inf values in the audio chunk
        chunk = self.replace_non_finite(chunk)

        # Calculate the RMS amplitude of the current chunk
        rms_amplitude = np.sqrt(np.mean(np.square(chunk)))
        print(f"RMS Amplitude: {rms_amplitude}")

        # Calculate the moving average of the last 10 amplitudes
        moving_average = self.calculate_moving_average()
        print(f"Moving Average of last 10 RMS values: {moving_average}")

        # Detect if the amplitude remains too high for too long
        if rms_amplitude > self.threshold:
            self.loud_duration += chunk_duration  # Add time if the noise is consistently loud
            print(f"Loud noise detected for {self.loud_duration} seconds")
        else:
            self.loud_duration = 0  # Reset loud duration if noise decreases

        # Gradually reduce external noise if it's been loud for too long
        if self.loud_duration > self.loud_threshold_duration:
            print("Reducing external noise as it has been loud for too long.")
            self.reduction_score = min(self.reduction_score + 0.05, 1.0)  # Increase reduction score gradually
        else:
            # Gradually allow outside sound back in if the noise is no longer loud
            self.reduction_score = max(self.reduction_score - 0.05, 0.0)

        print(f"Current reduction score: {self.reduction_score}")

        # Store the current RMS amplitude in the history
        self.previous_rms.append(rms_amplitude)

        # Skip processing if the amplitude is below the threshold
        if rms_amplitude < self.threshold:
            print("Amplitude below threshold, skipping processing.")
            return chunk

        print("Amplitude above threshold, processing audio...")

        # Apply the bandpass filter to isolate speech frequencies
        filtered_chunk = self.bandpass_filter(chunk, self.lowcut, self.highcut, self.sr)

        # Apply noise reduction to the chunk
        reduced_noise_chunk = nr.reduce_noise(y=filtered_chunk, sr=self.sr, prop_decrease=0.95)

        # Mix the original and reduced audio based on the dynamic reduction score
        final_chunk = (1 - self.reduction_score) * filtered_chunk + self.reduction_score * reduced_noise_chunk

        return final_chunk