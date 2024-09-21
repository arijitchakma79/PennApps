import pyaudio
import numpy as np
import threading
import queue
import wave
import os

class AudioOutput:
    def __init__(self, volume=1.0):
        # Initialize PyAudio
        self.__p = pyaudio.PyAudio()
        
        # Open a stream for audio output
        self.__stream = self.__p.open(format=pyaudio.paFloat32,
                                      channels=1,
                                      rate=16000,
                                      output=True)
        
        # Create a queue to hold audio data
        self.__queue = queue.Queue()
        
        # Set initial volume
        self.__volume = volume
        
        # Create and start a thread for playing audio
        self.__playThread = threading.Thread(target=self.__play_audio)
        self.__playThread.daemon = True
        self.__playThread.start()

    def add_sound_file(self, file_path, amplification=1.0):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        # Open the wave file
        with wave.open(file_path, 'rb') as wf:
            # Read all frames from the file
            data = wf.readframes(wf.getnframes())
            
            # Convert the audio data to float32 and normalize
            audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Apply amplification
            audio_data = audio_data * amplification
            
            # Clip the audio to prevent distortion
            audio_data = np.clip(audio_data, -1.0, 1.0)
            
            # Add the audio data to the queue
            self.__queue.put((audio_data, file_path))

    def __play_audio(self):
        while True:
            if not self.__queue.empty():
                # If there's audio in the queue, play it
                audio_data, file_path = self.__queue.get()
                
                # Apply volume control
                audio_data = audio_data * self.__volume
                
                # Play the audio
                self.__stream.write(audio_data.tobytes())
                
                # Delete the file
                try:
                    os.remove(file_path)
                    print(f"Played and deleted file: {file_path}")
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")
            else:
                # If the queue is empty, add a small silence to avoid blocking
                silence = np.zeros(1024, dtype=np.float32)
                self.__stream.write(silence.tobytes())

    def set_volume(self, volume):
        # Set the volume (0.0 to 1.0)
        self.__volume = max(0.0, min(1.0, volume))

    def get_volume(self):
        # Get the current volume
        return self.__volume

    def close(self):
        # Stop and close the audio stream
        self.__stream.stop_stream()
        self.__stream.close()
        
        # Terminate the PyAudio object
        self.__p.terminate()

# Example usage
if __name__ == "__main__":
    audio_output = AudioOutput()
    
    # Add some sound files to the queue
    audio_output.add_sound_file("sound1.wav")
    audio_output.add_sound_file("sound2.wav")
    
    # Keep the main thread running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping playback...")
        audio_output.close()