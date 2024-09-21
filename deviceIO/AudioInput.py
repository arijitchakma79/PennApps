import pyaudio
import numpy as np
import threading
import queue

from utils.constants import constants

class AudioInput:
    def __init__(self, callback, chunkDuration=0.2, channels=1):
        # Initialize audio input parameters
        self.__chunkDuration = chunkDuration
        self.__sampleRate = constants.AUDIO_SAMPLE_RATE
        self.__channels = channels
        self.__chunkSize = int(self.__sampleRate * chunkDuration)
        
        # Set up the audio recorder
        self.__init_recorder()
        self.__isProcessing = False
        self.__callback = callback
    
    def __init_recorder(self):
        # Initialize PyAudio and create a processing queue
        self.__audio = pyaudio.PyAudio()
        self.__stream = None
        self.__processingQueue = queue.Queue()
        self.__isRecording = False
    
    def __start_recording(self):
        # Start the audio stream for recording
        self.__isRecording = True
        self.__stream = self.__audio.open(
            format=pyaudio.paFloat32,
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
        # Callback function for the audio stream
        # Convert incoming audio data to numpy array and add to processing queue
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self.__processingQueue.put(audio_data)
        return (in_data, pyaudio.paContinue)
    
    def __start_processing(self):
        # Start a separate thread for processing audio data
        self.__isProcessing = True
        threading.Thread(target=self.__process_audio, daemon=True).start()
    
    def __stop_processing(self):
        # Stop the audio processing thread
        self.__isProcessing = False
    
    def __process_audio(self):
        # Main loop for processing audio data
        while self.__isProcessing:
            try:
                # Get audio chunk from queue and process it
                chunk = self.__processingQueue.get(timeout=1)
                self.__callback(chunk)
            except queue.Empty:
                # Continue if queue is empty (prevents blocking)
                continue
    
    def start(self):
        # Public method to start recording and processing
        self.__start_recording()
        self.__start_processing()
    
    def stop(self):
        # Public method to stop recording and processing
        self.__stop_recording()
        self.__stop_processing()