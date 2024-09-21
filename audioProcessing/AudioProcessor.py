from audioProcessing.NoiseFilter import NoiseReduction
import soundfile as sf
import librosa

from utils.constants import constants

class AudioProcessor:
    def __init__(self):
        self.__init_noise_filter()
          
    def __init_noise_filter(self):
        self.__lowcut = 300
        self.__highcut = 3400
        self.__threshold = 0.05
        self.__sr = constants.AUDIO_SAMPLE_RATE 

        self.__noiseReduction = NoiseReduction(self.__lowcut, self.__highcut, self.__threshold, self.__sr)

    def process_audio(self, fileName):
        chunkSize = self.__sr 
        audioData, sr = librosa.load(fileName, sr=self.__sr)

        processedAudio = self.__noiseReduction.process_chunk(audioData)
        sf.write(fileName, processedAudio, sr)