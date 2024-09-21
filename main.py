#from processing.ReductionController import ReductionController
from deviceIO.AudioInput import AudioInput
from deviceIO.AudioOutput import AudioOutput
from audioProcessing.AudioProcessor import AudioProcessor

import shutil
import time
import os

def process_callback(soundFile):
    #reductionFactor = reductionController.getReductionFactor()
    #print(reductionFactor)

    audioProcessor.process_audio(soundFile)
    audioOutput.add_sound_file(soundFile, amplification=30.0)

    stressLevel = 0.5
    #reductionController.update(stressLevel)

def prepareChunksDir():
    chunksDir = "chunks"
    if os.path.exists(chunksDir):
        shutil.rmtree(chunksDir)
    os.makedirs(chunksDir)

if __name__ == '__main__':
    print("Initial Commit.")
    prepareChunksDir()

    audioInput = AudioInput(process_callback, chunkDuration=0.2) 
    audioInput.start()

    audioOutput = AudioOutput(volume=1.0)
    #reductionController = ReductionController(0.3, 0.7)

    audioProcessor = AudioProcessor()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    audioOutput.close()
    audioInput.stop()