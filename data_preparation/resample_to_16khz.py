import os
import subprocess

source_dir = './raw_data/raw_audio_wav'
target_dir = './raw_data/raw_audio_16k'

# Iterate through all files
for file in os.listdir(source_dir):
    if file.endswith('.wav'):
        input_path = os.path.join(source_dir, file)
        output_path = os.path.join(target_dir, file)

        # Using ffmpeg to resample to 16khz
        command = ['ffmpeg', '-i', input_path, '-ar', '16000', '-af', 'aresample=async=1', output_path]

        try:
            # Run the command
            subprocess.run(command, check=True)

        except subprocess.CalledProcessError as e:
            print(f'Error resampling {file}: {e}')    

print("Resampling complete")            