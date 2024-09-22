import pyaudio
import cv2
import mediapipe as mp
import time
import numpy as np
from audio_chunk_processor import AudioChunkProcessor

class MicrophoneAudioHandler:
    def __init__(self, chunk_size=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100, 
                 background_music_file=None, bgm_volume=0.3, noise_threshold=10):
        """
        Initialize the audio handler with background music and amplitude threshold for noise.
        """
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.processor = AudioChunkProcessor(fs, chunk_size=chunk_size, 
                                             background_music_file=background_music_file, bgm_volume=bgm_volume, 
                                             noise_threshold=noise_threshold)
        self.p = pyaudio.PyAudio()

        # Initialize MediaPipe for person detection
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def start_stream(self):
        # Open the stream for audio input/output
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk_size)
    
    def stop_stream(self):
        # Close the audio stream
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def detect_person(self, frame):
        """
        Detect if a person is present in the frame using MediaPipe Pose detection.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb_frame)
        if result.pose_landmarks:
            print("Person is detected")
            return True
        return False

    def process_audio_stream(self):
        """
        Process audio from microphone, detect loud/uncomfortable sounds, and play background music.
        """
        print("Processing audio from microphone... Press Ctrl+C to stop.")
        self.start_stream()

        cap = cv2.VideoCapture(0)  # Open webcam for person detection

        try:
            while True:
                # Read a chunk of audio from the microphone
                audio_chunk = self.stream.read(self.chunk_size)

                # Capture video frame
                ret, frame = cap.read()
                if not ret:
                    break

                # Detect if a person is present in the video frame
                person_detected = self.detect_person(frame)

                # Process the chunk using the processor and the person detection status
                processed_chunk = self.processor.process_chunk(audio_chunk, person_detected)

                # Output the processed audio (background music or silence)
                self.stream.write(processed_chunk)

                # Show video frame
                cv2.imshow("Person Detection", frame)

                # Break the loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            print("Audio processing stopped.")
        finally:
            self.stop_stream()
            cap.release()
            cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    background_music_file = "background_music.wav"  # Path to background music
    bgm_volume = 0.3  # Volume of background music
    noise_threshold = 10  # Amplitude threshold for low sound detection (set to 10)
    
    mic_handler = MicrophoneAudioHandler(background_music_file=background_music_file, bgm_volume=bgm_volume, noise_threshold=noise_threshold)
    mic_handler.process_audio_stream()
