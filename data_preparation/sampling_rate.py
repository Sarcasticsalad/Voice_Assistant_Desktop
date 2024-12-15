import soundfile as sf
import os

audio_dir = './raw_data/raw_audio_16k'

def check_sample_rate(file_path):
    sample_rate = sf.read(file_path)
    print(f"Sample rate of {file_path}: {sample_rate} Hz")
    return sample_rate

for file in os.listdir(audio_dir):
    if file.endswith('.wav'):
        file_path = os.path.join(audio_dir, file)
        check_sample_rate(file_path)

