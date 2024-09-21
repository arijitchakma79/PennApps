from input.AudioInput import AudioInput
import time

if __name__ == '__main__':
    print("Initial Commit.")

    audio_input = AudioInput(chunkDuration=2) 
    audio_input.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    audio_input.stop()