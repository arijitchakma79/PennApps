from deviceIO.AudioInput import AudioInput
from deviceIO.AudioOutput import AudioOutput
import time

import shutil
import os

def process_callback(soundFile):
    audioOutput.add_sound_file(soundFile, amplification=30.0)

if __name__ == '__main__':
    print("Initial Commit.")

    chunksDir = "chunks"
    if os.path.exists(chunksDir):
        shutil.rmtree(chunksDir)
    os.makedirs(chunksDir)

    audioInput = AudioInput(process_callback, chunkDuration=0.2) 
    audioInput.start()

    audioOutput = AudioOutput(volume=1.0)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    audioOutput.close()
    audioInput.stop()