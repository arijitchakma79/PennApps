# Import necessary modules for audio input, output, and processing
from deviceIO.AudioInput import AudioInput
from deviceIO.AudioOutput import AudioOutput
#from audioProcessing.AudioProcessor import AudioProcessor
import time

from utils.constants import constants
from audioProcessing.AmplitudeAnalyzer import AmplitudeAnalyzer
from processing.FaceDetector import FaceDetector

# Callback function to process incoming audio data
def process_callback(audio_data):
    threshold, amplitude, variance = amplitudeAnalyzer.process_chunk(audio_data)

    if(variance >= 7.5 or faceDetector.is_face_detected()):
        print("Important!")

    #processed_audio = audioProcessor.process_audio(audio_data)
    #audioOutput.add_audio_data(processed_audio, amplification=30.0)

def face_callback(face_detected):
    if(face_detected):
        print("important!")
    #print("Face detected ", face_detected)
    pass

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

    faceDetector = FaceDetector(face_callback)
    faceDetector.start()

    print("Started...")
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
        faceDetector.stop()