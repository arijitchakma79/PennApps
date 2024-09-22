# Import necessary modules for audio input, output, and processing
from deviceIO.AudioInput import AudioInput
from deviceIO.AudioOutput import AudioOutput
#from audioProcessing.AudioProcessor import AudioProcessor
import time

from utils.constants import constants
from audioProcessing.AmplitudeAnalyzer import AmplitudeAnalyzer

from deviceIO.camera import Camera
import cv2


import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize the face detection model
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

while True:
    camera = Camera()
    frame = camera.captureFrame()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite("frame.jpg", frame) 

    results = face_detection.process(rgb_frame)

    # Draw face detections
    if results.detections:
        if(len(results.detections) > 0):
            print("Face detected")


# Callback function to process incoming audio data
def process_callback(audio_data):
    print(amplitudeAnalyzer.process_chunk(audio_data))

    #processed_audio = audioProcessor.process_audio(audio_data)
    #audioOutput.add_audio_data(processed_audio, amplification=30.0)

# Main execution block
if __name__ == '__main__':
    print("Starting real-time audio processing...")
    
    # Initialize AudioInput with the process_callback function
    # Set chunk duration to 0.2 seconds
    audioInput = AudioInput(process_callback, chunkDuration=constants.AUDIO_CHUNK_SIZE)
    audioInput.start()
    
    # Initialize AudioOutput with default volume
    audioOutput = AudioOutput(volume=1.0)
    
    # Create an instance of AudioProcessor for audio processing
    #audioProcessor = AudioProcessor()

    amplitudeAnalyzer = AmplitudeAnalyzer(9000)
    camera = Camera()

    frame = camera.captureFrame()
    cv2.imwrite("frame.jpg", frame)
    print("frame")

    try:
        # Main processing loop
        while True:
            # Sleep briefly to prevent excessive CPU usage
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Handle user interruption (e.g., Ctrl+C)
        print("Stopping audio processing...")
    finally:
        # Cleanup: close audio output and stop audio input
        audioOutput.close()
        audioInput.stop()