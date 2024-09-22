import pyaudio
import wave
import threading
import numpy as np

class MusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.playing = False
        self.volume = 1.0
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.wf = wave.open(self.filename, 'rb')
        self.thread = None
        self.lock = threading.Lock()

    def play_loop(self):
        def callback(in_data, frame_count, time_info, status):
            data = self.wf.readframes(frame_count)
            if len(data) < frame_count * self.wf.getsampwidth() * self.wf.getnchannels():
                self.wf.rewind()
                data += self.wf.readframes(frame_count - len(data) // (self.wf.getsampwidth() * self.wf.getnchannels()))
            
            with self.lock:
                data = self._adjust_volume(data)
            return (data, pyaudio.paContinue)
        
        self.stream = self.pa.open(format=self.pa.get_format_from_width(self.wf.getsampwidth()),
                                   channels=self.wf.getnchannels(),
                                   rate=self.wf.getframerate(),
                                   output=True,
                                   stream_callback=callback)
        
        self.stream.start_stream()
        self.playing = True
        
        while self.playing and self.stream.is_active():
            threading.Event().wait(0.1)
        
        self.stream.stop_stream()
        self.stream.close()
        self.wf.rewind()

    def start(self):
        if not self.playing:
            self.thread = threading.Thread(target=self.play_loop)
            self.thread.start()

    def stop(self):
        self.playing = False
        if self.thread:
            self.thread.join()

    def set_volume(self, volume):
        with self.lock:
            self.volume = max(0.0, min(1.0, volume))

    def _adjust_volume(self, data):
        array = np.frombuffer(data, dtype=np.int16)
        array = (array * self.volume).astype(np.int16)
        return array.tobytes()

    def __del__(self):
        self.stop()
        self.pa.terminate()