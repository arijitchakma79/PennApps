from input.AudioInput import AudioInput

if __name__ == '__main__':
    print("Initial Commit.")


    audio_input = AudioInput(chunkDuration=2) 
    audio_input.run()