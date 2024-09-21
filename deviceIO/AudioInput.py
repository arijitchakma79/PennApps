import pyaudio
import numpy as np
import threading
import queue
import wave

class AudioInput:
    def __init__(self, callback, chunkDuration=10, sampleRate=44100, channels=1, chunkSize=1024):
        # Initialize audio parameters
        self.__chunkDuration = chunkDuration
        self.__sampleRate = sampleRate
        self.__channels = channels
        self.__chunkSize = chunkSize
        
        self.__init_recorder()
        self.__isProcessing = False

        self.__callback = callback
    
    def __init_recorder(self):
        # Set up PyAudio and audio stream
        self.__audio = pyaudio.PyAudio()
        self.__stream = None
        
        # Initialize buffer, lock, and processing queue
        self.__buffer = []
        self.__bufferLock = threading.Lock()
        self.__processingQueue = queue.Queue()
        
        self.__chunkCounter = 0
        self.__isRecording = False
    
    def __start_recording(self):
        # Configure and start the audio stream
        self.__isRecording = True
        self.__stream = self.__audio.open(
            format=pyaudio.paInt16,
            channels=self.__channels,
            rate=self.__sampleRate,
            input=True,
            frames_per_buffer=self.__chunkSize,
            stream_callback=self.__audio_callback
        )
        self.__stream.start_stream()
    
    def __stop_recording(self):
        # Stop and clean up the audio stream
        self.__isRecording = False
        if self.__stream:
            self.__stream.stop_stream()
            self.__stream.close()
        self.__audio.terminate()
    
    def __audio_callback(self, in_data, frame_count, time_info, status):
        # Process incoming audio data
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        with self.__bufferLock:
            self.__buffer.extend(audio_data)
            required_buffer_size = int(self.__chunkDuration * self.__sampleRate * self.__channels)
            
            # If buffer is full, extract a chunk and add to processing queue
            if len(self.__buffer) >= required_buffer_size:
                chunk = self.__buffer[:required_buffer_size]
                self.__buffer = self.__buffer[required_buffer_size:]
                self.__processingQueue.put(chunk)
        
        return (in_data, pyaudio.paContinue)
    
    def __start_processing(self):
        # Start the audio processing thread
        self.__isProcessing = True
        threading.Thread(target=self.__process_audio, daemon=True).start()
    
    def __stop_processing(self):
        self.__isProcessing = False
    
    def __process_audio(self):
        while self.__isProcessing:
            try:
                # Get and process audio chunk
                chunk = self.__processingQueue.get(timeout=1)
                chunk_array = np.array(chunk, dtype=np.int16)
                
                # Save chunk as WAV file
                filename = f"chunks/chunk_{self.__chunkCounter}.wav"
                self.__chunkCounter += 1
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(self.__channels)
                    wf.setsampwidth(self.__audio.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(self.__sampleRate)
                    wf.writeframes(chunk_array.tobytes())

                print(f"Saved chunk to {filename}")
                self.__callback(filename)

            except queue.Empty:
                continue
    
    def start(self):
        # Start recording and processing
        self.__start_recording()
        self.__start_processing()
    
    def stop(self):
        # Stop recording and processing
        self.__stop_recording()
        self.__stop_processing()