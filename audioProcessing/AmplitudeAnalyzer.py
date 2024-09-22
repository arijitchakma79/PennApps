import numpy as np

class AmplitudeAnalyzer:
    def __init__(self, amplitudeThreshold=500):
        self.__amplitudeThreshold = amplitudeThreshold

    def process_chunk(self, chunk):
        audioData = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)

        amplitude = np.sqrt(np.mean(np.square(audioData)))

        return amplitude <= self.__amplitudeThreshold, amplitude