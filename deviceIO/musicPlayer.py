import pyaudio
import wave
import threading
import numpy

class MusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.playing = False
        self.volume = 1.0
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.wf = wave.open(self.filename, 'rb')
        
    def play(self):
        def callback(in_data, frame_count, time_info, status):
            data = self.wf.readframes(frame_count)
            if len(data) < frame_count * self.wf.getsampwidth() * self.wf.getnchannels():
                self.wf.rewind()
                data += self.wf.readframes(frame_count - len(data) // (self.wf.getsampwidth() * self.wf.getnchannels()))
            
            # Apply volume
            data = self._adjust_volume(data)
            return (data, pyaudio.paContinue)
        
        self.stream = self.pa.open(format=self.pa.get_format_from_width(self.wf.getsampwidth()),
                                   channels=self.wf.getnchannels(),
                                   rate=self.wf.getframerate(),
                                   output=True,
                                   stream_callback=callback)
        
        self.stream.start_stream()
        self.playing = True
        
        while self.stream.is_active():
            threading.Event().wait(0.1)
        
        self.stop()
    
    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.playing = False
        self.wf.rewind()
    
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
    
    def _adjust_volume(self, data):
        # Convert to integer array
        array = numpy.frombuffer(data, dtype=numpy.int16)
        # Adjust volume
        array = (array * self.volume).astype(numpy.int16)
        # Convert back to bytes
        return array.tobytes()
    
    def __del__(self):
        self.stop()
        if self.pa:
            self.pa.terminate()