# Import necessary modules for audio input, output, and processing
from deviceIO.AudioInput import AudioInput
from deviceIO.AudioOutput import AudioOutput
from audioProcessing.AudioProcessor import AudioProcessor
import time

# Callback function to process incoming audio data
def process_callback(audio_data):
    # Process the audio data using the AudioProcessor
    processed_audio = audioProcessor.process_audio(audio_data)
    # Add the processed audio to the output stream with amplification
    audioOutput.add_audio_data(processed_audio, amplification=30.0)

# Main execution block
if __name__ == '__main__':
    print("Starting real-time audio processing...")
    
    # Initialize AudioInput with the process_callback function
    # Set chunk duration to 0.2 seconds
    audioInput = AudioInput(process_callback, chunkDuration=0.2)
    audioInput.start()
    
    # Initialize AudioOutput with default volume
    audioOutput = AudioOutput(volume=1.0)
    
    # Create an instance of AudioProcessor for audio processing
    audioProcessor = AudioProcessor()
    
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