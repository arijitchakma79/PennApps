import numpy as np

class AmplitudeAnalyzer:
    def __init__(self, amplitudeThreshold=500):
        self.__amplitudeThreshold = amplitudeThreshold
    
    def process_chunk(self, chunk):
        audioData = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)
        
        # Calculate RMS amplitude
        rms_amplitude = np.sqrt(np.mean(np.square(audioData)))
        
        # Calculate peak-to-peak amplitude
        peak_to_peak = np.ptp(audioData)
        
        # Calculate crest factor
        if rms_amplitude != 0:
            crest_factor = peak_to_peak / (2 * rms_amplitude)
        else:
            crest_factor = 0
        
        return rms_amplitude >= self.__amplitudeThreshold, rms_amplitude, crest_factor