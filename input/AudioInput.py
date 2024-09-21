import pyaudio
import numpy as np
import threading
import queue
import wave
import time

class AudioInput:
    def __init__(self, chunkDuration=10, sampleRate=44100, channels=1, chunkSize=1024):
        self.__chunkDuration = chunkDuration
        self.__sampleRate = sampleRate
        self.__channels = channels
        self.__chunkSize = chunkSize
        
        self.__init_recorder()
        self.__isProcessing = False
    
    def __init_recorder(self):
        self.__audio = pyaudio.PyAudio()
        self.__stream = None

        self.__buffer = []
        self.__bufferLock = threading.Lock()
        self.__processingQueue = queue.Queue()

        self.__chunkCounter = 0  # Counter for chunk files
        self.__isRecording = False
    
    def __start_recording(self):
        self.__isRecording = True
        self.__stream = self.__audio.open(
            format=pyaudio.paInt16,  # Use 16-bit integer format
            channels=self.__channels,
            rate=self.__sampleRate,
            input=True,
            frames_per_buffer=self.__chunkSize,
            stream_callback=self.__audio_callback
        )
        self.__stream.start_stream()
    
    def __stop_recording(self):
        self.__isRecording = False
        if self.__stream:
            self.__stream.stop_stream()
            self.__stream.close()
        self.__audio.terminate()

    def __audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        with self.__bufferLock:
            self.__buffer.extend(audio_data)
            required_buffer_size = int(self.__chunkDuration * self.__sampleRate * self.__channels)
            if len(self.__buffer) >= required_buffer_size:
                chunk = self.__buffer[:required_buffer_size]
                self.__buffer = self.__buffer[required_buffer_size:]
                self.__processingQueue.put(chunk)
        return (in_data, pyaudio.paContinue)

    def __start_processing(self):
        self.__isProcessing = True
        threading.Thread(target=self.__process_audio, daemon=True).start()

    def __stop_processing(self):
        self.__isProcessing = False

    def __process_audio(self):
        while self.__isProcessing:
            try:
                chunk = self.__processingQueue.get(timeout=1)
                # Save the chunk to a WAV file
                chunk_array = np.array(chunk, dtype=np.int16)
                filename = f"chunk_{self.__chunkCounter}.wav"
                self.__chunkCounter += 1
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(self.__channels)
                    wf.setsampwidth(self.__audio.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(self.__sampleRate)
                    wf.writeframes(chunk_array.tobytes())
                print(f"Saved chunk to {filename}")
            except queue.Empty:
                continue

    def start(self):
        self.__start_recording()
        self.__start_processing()

    def stop(self):
        self.__stop_recording()
        self.__stop_processing()

    def run(self):
        self.start()
        try:
            while self.__isRecording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self.stop()