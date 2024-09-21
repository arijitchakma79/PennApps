import numpy as np
import librosa
import noisereduce as nr
import soundfile as sf
from scipy.signal import butter, lfilter

class NoiseReduction:
    def __init__(self, input_file_path, output_file_path, lowcut, highcut, threshold, sr):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.lowcut = lowcut
        self.highcut = highcut
        self.threshold = threshold
        self.sr = sr

    def butter_bandpass(self, fs, order=3):
        nyquist = 0.5 * fs
        low = self.lowcut / nyquist
        high = self.highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a
    
    def bandpass_filter(self, data, fs, order=3):
        b, a = self.butter_bandpass(fs, order=order)
        y = lfilter(b, a, data)
        return y
    
    def process_sound(self):
        audio_data, sr = librosa.load(self.input_file_path, sr=self.sr)
        
        rms_amplitude = np.sqrt(np.mean(np.square(audio_data)))
        print(f"RMS Amplitude: {rms_amplitude}")
        
        # Skip processing if the amplitude is below the threshold
        if rms_amplitude < self.threshold:
            print("Amplitude below threshold, skipping processing.")
            return audio_data
        
        print("Amplitude above threshold, processing audio...")

        # Apply bandpass filter
        filtered_audio = self.bandpass_filter(audio_data, sr)
        
        # Apply noise reduction
        reduced_noise_audio = nr.reduce_noise(y=filtered_audio, sr=sr, prop_decrease=0.8)

        # Save the processed audio
        sf.write(self.output_file_path, reduced_noise_audio, sr)
        print(f"Processed audio saved to {self.output_file_path}")

        return reduced_noise_audio


if __name__ == "__main__":
    input_file_path = "eme.wav"
    output_file_path = "processed_audio.wav"
    lowcut = 500
    highcut = 1500
    threshold = 0.01
    sr = 44100

    noise_reduction = NoiseReduction(input_file_path, output_file_path, lowcut, highcut, threshold, sr)
    noise_reduction.process_sound()