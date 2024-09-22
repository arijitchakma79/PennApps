# Import necessary modules for audio input, output, and processing
from deviceIO.AudioInput import AudioInput
#from deviceIO.AudioOutput import AudioOutput
from deviceIO.musicPlayer import MusicPlayer
#from audioProcessing.AudioProcessor import AudioProcessor
import time

from utils.constants import constants
from utils.console import Console

from audioProcessing.AmplitudeAnalyzer import AmplitudeAnalyzer
from processing.FaceDetector import FaceDetector

from rich.live import Live
from rich.table import Table
from rich import box

from deviceIO.Device import Device

def generate_table(data):
    table = Table(box=box.SIMPLE)
    table.add_column("Metric")
    table.add_column("Value")
    
    for key, value in data.items():
        table.add_row(key, str(value))
    
    return table

data = {
    "Amplitude": 0,
    "Variance": 0,
    "Threshold": False,
    "FaceDetected" : False,
    "CurrentVolume": 0,
    "TargetVolume": 0,
    "ReferenceVolume":0
}

musicVolume = 1.0
targetMusicVolume = 1.0
volumeSpeed = 0.1
referenceVolume = 0

counter = 0
# Callback function to process incoming audio data
def process_callback(audio_data):
    global targetMusicVolume, counter
    threshold, amplitude, variance = amplitudeAnalyzer.process_chunk(audio_data)

    data["Amplitude"] = amplitude
    data["Variance"] = variance
    data["Threshold"] = threshold

    if(variance >= 7.5 or faceDetector.is_face_detected()):
        #musicPlayer.set_volume(0.3)
        #print("Important!")
        targetMusicVolume = 0.1
        counter = 0
    else:
        counter+=1
        if(counter >= 8):
            targetMusicVolume = 1.0

    #processed_audio = audioProcessor.process_audio(audio_data)
    #audioOutput.add_audio_data(processed_audio, amplification=30.0)

def face_callback(face_detected):
    data["FaceDetected"] = face_detected

    #if(face_detected):
        #print("important!")
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
    # audioOutput = AudioOutput(volume=1.0)
    
    # Create an instance of AudioProcessor for audio processing
    #audioProcessor = AudioProcessor()

    amplitudeAnalyzer = AmplitudeAnalyzer(9000)

    faceDetector = FaceDetector(face_callback)
    faceDetector.start()

    musicPlayer = MusicPlayer("calm.wav")
    musicPlayer.start()

    device = Device()

    print("Started...")

    Console.clear_screen()
    Console.create_clean_area(11)

    try:
        with Live(generate_table(data), refresh_per_second=2) as live:
            # Main processing loop
            while True:
                # Sleep briefly to prevent excessive CPU usage
                time.sleep(0.05)

                target = max(0.0, min(1.0, targetMusicVolume + referenceVolume))
                deltaVolume = target - musicVolume
                deltaVolume *= volumeSpeed

                musicVolume += deltaVolume
                musicVolume = max(0.0, min(1.0, musicVolume))

                musicPlayer.set_volume(musicVolume)

                data["CurrentVolume"] = musicVolume
                data["TargetVolume"] = target
                data["ReferenceVolume"] = referenceVolume
            
                live.update(generate_table(data))

                if(device.is_button1_pressed()):
                    print("Reference music volume is increased by 0.1") 
                    referenceVolume += 0.1

                    while(device.is_button1_pressed()):
                        pass

                if(device.is_button2_pressed()):
                    print("Reference music volume is decreased by 0.1") 
                    referenceVolume -= 0.1

                    while(device.is_button2_pressed()):
                        pass


    except KeyboardInterrupt:
        # Handle user interruption (e.g., Ctrl+C)
        print("Stopping audio processing...")
    finally:
        # Cleanup: close audio output and stop audio input
        #audioOutput.close()
        audioInput.stop()
        faceDetector.stop()