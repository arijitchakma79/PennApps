from audioProcessing.NoiseFilter import NoiseReduction
from utils.constants import constants

class AudioProcessor:
    def __init__(self):
        # Initialize the noise filter when creating an AudioProcessor instance
        self.__init_noise_filter()
    
    def __init_noise_filter(self):
        # Set up parameters for the noise filter
        self.__lowcut = 300  # Lower frequency cutoff in Hz
        self.__highcut = 3400  # Upper frequency cutoff in Hz
        self.__threshold = 0.05  # Noise threshold for reduction
        self.__sr = constants.AUDIO_SAMPLE_RATE  # Sample rate from constants

        # Create a NoiseReduction instance with the specified parameters
        self.__noiseReduction = NoiseReduction(self.__lowcut, self.__highcut, self.__threshold, self.__sr)

    def process_audio(self, audio_data):
        # Process the input audio data using the noise reduction filter
        return self.__noiseReduction.process_chunk(audio_data)