from deviceIO.AudioInput import AudioInput
from deviceIO.AudioOutput import AudioOutput
import time

def process_callback(soundFile):
    audioOutput.add_sound_file(soundFile)

if __name__ == '__main__':
    print("Initial Commit.")

    audioInput = AudioInput(process_callback, chunkDuration=1) 
    audioInput.start()

    audioOutput = AudioOutput()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    audioInput.stop()