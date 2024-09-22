# SoundShield: Dynamic Noise Management System

SoundShield is a dynamic wearable device designed to help individuals, particularly those with autism and hyperacusis, manage sensory overload caused by noise pollution. The system automatically adapts to the surrounding environment, playing calming background music when needed and filtering out unwanted noise, while keeping users connected to important sounds like human speech. Additionally, the system uses computer vision to detect if a person is behind the user and provides alerts, helping users stay aware of their surroundings.

## Features
1. **Real-time audio processing** to dynamically adjust background noise and reduce sensory overload.
2. **Calming background music** automatically plays when the noise level becomes overwhelming.
3. **Person detection** using computer vision to alert users if someone is behind them.
4. **Seamless audio filtering** ensures users are aware of important sounds, such as human speech.
5. Designed to help individuals with **autism**, **hyperacusis**, and **sensory sensitivities**, as well as **elderly individuals**, **students**, and **commuters**.

## Table of Contents
- [Inspiration](#inspiration)
- [How it works](#how-it-works)
- [Hardware Requirements](#hardware-requirements)
- [Software Setup](#software-setup)
- [How to Run the Project](#how-to-run-the-project)
- [Challenges](#challenges)
- [Accomplishments](#accomplishments)
- [Future Enhancements](#future-enhancements)

## Inspiration
Noise sensitivity is common in individuals with **autism** and **hyperacusis**, and it can significantly impact their quality of life. Studies show that **50-70% of autistic individuals** experience hypersensitivity to everyday sounds, often leading to anxiety, stress, and avoidance of social situations. SoundShield was inspired by the need to create a **dynamic, adaptive system** that helps individuals manage noise levels without feeling isolated from the outside world.

## How it works
SoundShield continuously processes audio input from the environment, adjusting sound levels based on real-time conditions:
1. **Audio Input**: A microphone captures the surrounding noise.
2. **Real-Time Audio Processing**:
   - **Noise reduction**: Filters out loud, overwhelming sounds using techniques like **spectral subtraction** and **dynamic range compression**.
   - **Calming background music**: Automatically plays when the noise level exceeds a certain threshold (e.g., amplitude > 1000).
3. **Person Detection**: The camera detects if someone is behind the user and stops the background music if both low noise and a person are detected.
4. **Output**: The processed sound is played through the headphones.

## Hardware Requirements
- **Raspberry Pi Zero** (or any other compatible device)
- **Microphone** for capturing audio input
- **Headphones** for audio output
- **Camera** for person detection
- **Optional**: Heart rate sensor for future stress detection feature

## Software Setup
### 1. Install Dependencies
You need to install the required Python libraries before running the project. Here's a list of dependencies:

- Python 3.x
- `pyaudio` for audio input/output
- `librosa` for audio processing
- `opencv-python` for computer vision
- `mediapipe` for pose detection
- `numpy` for numerical computations
- `soundfile` for handling audio files
- `scipy` for signal processing

To install the dependencies, run:
```bash
pip install pyaudio numpy librosa opencv-python mediapipe soundfile scipy
```
### 2. Background Music Setup
You'll need a WAV file for background music, which will be played when the noise level exceeds the threshold. Place the music file in the project directory or provide its path during initialization. Below is the code that handles loading and playing background music.

### How to Run the Project
1. Clone the repository:
```bash
git clone https://github.com/arijitchakma79/PennApps2024.git
cd SoundShield
```
2. Run the main application:
 ```bash
python3 main.py
```
3. Adjust Parameters:
You can adjust the parameters such as **noise_threshold**, **bgm_volume**, and **chunk_size** in the microphone_audio_handler.py file to fine-tune the system based on your environment and personal needs.

### Challenges
1. Real-time processing: Ensuring smooth real-time audio and video processing on resource-constrained devices like the Raspberry Pi Zero was challenging due to its limited computing power. Processing both the audio filtering and the camera-based person detection simultaneously required optimization.

2. Noise classification: Differentiating between human speech and other noises to avoid filtering out important sounds while reducing ambient noise proved difficult. Tuning the noise reduction algorithms without affecting speech clarity was a major hurdle.

3. Hardware limitations: Integrating the camera and audio system on a small, low-power device like the Raspberry Pi Zero required balancing performance with real-time needs. Achieving 4. smooth user experience while ensuring low latency was key.

4. Dynamic sound control: Designing a system that intelligently transitions between filtering, playing music, and alerting based on environmental conditions, without overwhelming the user, required thoughtful system design.

### Accomplishments
-  Successfully integrated real-time audio processing with computer vision, providing an adaptive noise management system.
- Developed a wearable that dynamically adjusts background music and filters noise, helping individuals with autism and hyperacusis cope with sensory overload in noisy environments.
- Interdisciplinary integration of audio processing and computer vision, managing both in real-time, requires deep knowledge in both fields.

### Future Enhancements
1. ***Heart Rate Sensor Integration***: Add a heart rate sensor to detect stress and adjust the noise reduction score accordingly, playing calming music when the user becomes stressed.
2. ***Improved Sound Classification***: Enhance the system’s ability to distinguish between human speech and other noises, so it better filters unwanted noise while preserving conversations.
3. ***Advanced User Interface:*** Develop a mobile or desktop application to control SoundShield settings and provide visual feedback.
4. ***Increased Computing Power***: Explore more powerful hardware to enhance real-time processing capabilities, especially for complex environments.
5. ***Custom Soundscapes***: Allow users to upload personalized soundscapes, making the experience more customizable and tailored to individual needs.
