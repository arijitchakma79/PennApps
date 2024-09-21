import numpy as np
import noisereduce as nr
import sounddevice as sd
import soundfile as sf
import librosa
from scipy.signal import butter, lfilter

class NoiseReduction:
    def __init__(self, lowcut, highcut, threshold, sr):
        self.lowcut = lowcut
        self.highcut = highcut
        self.threshold = threshold
        self.sr = sr

    def butter_bandpass(self, fs, order=5):  # Higher-order filter for accuracy
        nyquist = 0.5 * fs
        low = self.lowcut / nyquist
        high = self.highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, fs, order=10):  # Higher order for better filtering accuracy
        b, a = self.butter_bandpass(fs, order=order)
        y = lfilter(b, a, data)
        return y

    def process_chunk(self, chunk):
        # Calculate the RMS amplitude of the chunk
        rms_amplitude = np.sqrt(np.mean(np.square(chunk)))
        print(f"RMS Amplitude: {rms_amplitude}")

        # Skip processing if the amplitude is below the threshold
        if rms_amplitude < self.threshold:
            print("Amplitude below threshold, skipping processing.")
            return chunk

        print("Amplitude above threshold, processing audio...")

        # Apply the bandpass filter to isolate the speech frequencies
        filtered_chunk = self.bandpass_filter(chunk, self.sr)

        # Apply noise reduction to the chunk
        reduced_noise_chunk = nr.reduce_noise(y=filtered_chunk, sr=self.sr, prop_decrease=0.95)

        return reduced_noise_chunk


def process_audio_in_chunks(audio_data, chunk_size, noise_reduction):
    # Split the audio data into chunks
    chunks = [audio_data[i:i + chunk_size] for i in range(0, len(audio_data), chunk_size)]
    processed_audio = []

    # Process each chunk
    for chunk in chunks:
        processed_chunk = noise_reduction.process_chunk(chunk)
        processed_audio.append(processed_chunk)

    # Concatenate the processed chunks
    return np.concatenate(processed_audio)