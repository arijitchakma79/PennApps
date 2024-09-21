import pyaudio
import numpy as np
import threading
import queue
import wave

class AudioOutput:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  output=True)
        self.queue = queue.Queue()
        self.play_thread = threading.Thread(target=self._play_audio)
        self.play_thread.daemon = True
        self.play_thread.start()

    def add_sound_file(self, file_path):
        with wave.open(file_path, 'rb') as wf:
            data = wf.readframes(wf.getnframes())
            audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            self.queue.put(audio_data)

    def _play_audio(self):
        while True:
            if not self.queue.empty():
                audio_data = self.queue.get()
                self.stream.write(audio_data.tobytes())
            else:
                # If the queue is empty, add a small silence to avoid blocking
                silence = np.zeros(1024, dtype=np.float32)
                self.stream.write(silence.tobytes())

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()