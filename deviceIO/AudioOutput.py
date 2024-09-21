import pyaudio
import numpy as np
import threading
import queue
import wave

class AudioOutput:
    def __init__(self):
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        
        # Open a stream for audio output
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  output=True)
        
        # Create a queue to hold audio data
        self.queue = queue.Queue()
        
        # Create and start a thread for playing audio
        self.play_thread = threading.Thread(target=self._play_audio)
        self.play_thread.daemon = True
        self.play_thread.start()

    def add_sound_file(self, file_path):
        # Open the wave file
        with wave.open(file_path, 'rb') as wf:
            # Read all frames from the file
            data = wf.readframes(wf.getnframes())
            
            # Convert the audio data to float32 and normalize
            audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Add the audio data to the queue
            self.queue.put(audio_data)

    def _play_audio(self):
        while True:
            if not self.queue.empty():
                # If there's audio in the queue, play it
                audio_data = self.queue.get()
                self.stream.write(audio_data.tobytes())
            else:
                # If the queue is empty, add a small silence to avoid blocking
                silence = np.zeros(1024, dtype=np.float32)
                self.stream.write(silence.tobytes())

    def close(self):
        # Stop and close the audio stream
        self.stream.stop_stream()
        self.stream.close()
        
        # Terminate the PyAudio object
        self.p.terminate()