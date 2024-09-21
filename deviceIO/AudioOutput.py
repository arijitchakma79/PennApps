import pyaudio
import numpy as np
import threading
import queue

from utils.constants import constants

class AudioOutput:
    def __init__(self, volume=1.0):
        # Initialize PyAudio
        self.__p = pyaudio.PyAudio()
        
        # Open an output stream
        self.__stream = self.__p.open(format=pyaudio.paFloat32,
                                      channels=1,
                                      rate=constants.AUDIO_SAMPLE_RATE,
                                      output=True)
        
        # Create a queue for audio data
        self.__queue = queue.Queue()
        
        # Set initial volume
        self.__volume = volume
        
        # Start a separate thread for audio playback
        self.__playThread = threading.Thread(target=self.__play_audio)
        self.__playThread.daemon = True
        self.__playThread.start()

    def add_audio_data(self, audio_data, amplification=1.0):
        # Apply amplification and volume control to the audio data
        processed_data = audio_data * amplification * self.__volume
        
        # Clip the audio to prevent distortion
        processed_data = np.clip(processed_data, -1.0, 1.0)
        
        # Add the processed data to the playback queue
        self.__queue.put(processed_data)

    def __play_audio(self):
        # Continuous loop for audio playback
        while True:
            if not self.__queue.empty():
                # Get and play audio data from the queue
                audio_data = self.__queue.get()
                self.__stream.write(audio_data.tobytes())
            else:
                # If the queue is empty, play a small silence to avoid blocking
                silence = np.zeros(1024, dtype=np.float32)
                self.__stream.write(silence.tobytes())

    def set_volume(self, volume):
        # Set volume, ensuring it's between 0 and 1
        self.__volume = max(0.0, min(1.0, volume))

    def get_volume(self):
        # Get current volume
        return self.__volume

    def close(self):
        # Clean up resources
        self.__stream.stop_stream()
        self.__stream.close()
        self.__p.terminate()