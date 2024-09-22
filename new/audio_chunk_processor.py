import pyaudio
import numpy as np
import librosa
import time
from scipy.signal import butter, lfilter

class AudioChunkProcessor:
    def __init__(self, fs, chunk_size=1024, background_music_file=None, bgm_volume=0.3, noise_threshold=500):
        """
        Parameters:
        background_music_file: Path to the background music.
        bgm_volume: Volume of background music relative to microphone input.
        noise_threshold: Threshold for amplitude below which the music should pause if a person is detected.
        """
        self.fs = fs
        self.chunk_size = chunk_size
        self.bgm_volume = bgm_volume
        self.noise_threshold = noise_threshold  # Set the low amplitude threshold
        self.bgm_playing = True  # Music plays by default
        self.last_pause_time = 0  # Keep track of the last time music was paused

        # Load background music
        if background_music_file:
            print(f"Loading background music from {background_music_file}")
            self.load_background_music(background_music_file)

    def load_background_music(self, background_music_file):
        try:
            # Load background music using librosa
            self.bgm_data, _ = librosa.load(background_music_file, sr=self.fs)
            print(f"Background music loaded successfully with {len(self.bgm_data)} samples.")
            self.bgm_data = np.pad(self.bgm_data, (0, max(0, self.chunk_size - len(self.bgm_data) % self.chunk_size)), mode='wrap')
            self.bgm_index = 0  # Track background music position
        except Exception as e:
            print(f"Error loading background music: {e}")

    def get_next_bgm_chunk(self):
        """
        Get the next chunk of background music data to play.
        """
        start_index = self.bgm_index
        end_index = start_index + self.chunk_size
        if end_index >= len(self.bgm_data):
            end_index = end_index % len(self.bgm_data)
        bgm_chunk = self.bgm_data[start_index:end_index]
        self.bgm_index = end_index % len(self.bgm_data)
        return bgm_chunk

    def detect_noise_level(self, audio_data):
        """
        Detect if the amplitude of the sound is below the threshold (too quiet).
        """
        amplitude = np.sqrt(np.mean(np.square(audio_data)))  # RMS amplitude
        print(f"Detected amplitude: {amplitude}")  # Debugging
        return amplitude <= self.noise_threshold

    def process_chunk(self, chunk, person_detected):
        """
        Process the audio chunk and play background music if conditions are met.
        Stop the music for 5 seconds if a person is detected and sound amplitude is below the threshold.
        """
        audio_data = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)

        # Check if amplitude is too low
        low_amplitude_detected = self.detect_noise_level(audio_data)

        # Pause the music for 5 seconds if amplitude is low and a person is detected
        current_time = time.time()
        if low_amplitude_detected and person_detected and current_time - self.last_pause_time > 5:
            print("Low amplitude detected and person detected, pausing music for 5 seconds.")
            self.bgm_playing = False
            self.last_pause_time = current_time

        # If music was paused for 5 seconds, resume it
        if current_time - self.last_pause_time >= 5:
            self.bgm_playing = True

        # If background music is playing, output it; otherwise, output silence
        if self.bgm_playing and hasattr(self, 'bgm_data'):  # Check if background music is loaded
            bgm_chunk = self.get_next_bgm_chunk()
            bgm_chunk = np.clip(bgm_chunk * self.bgm_volume, -1, 1)  # Ensure no overflow
            return (bgm_chunk * 32767).astype(np.int16).tobytes()
        else:
            # Output silence during the pause
            return np.zeros(self.chunk_size, dtype=np.int16).tobytes()
