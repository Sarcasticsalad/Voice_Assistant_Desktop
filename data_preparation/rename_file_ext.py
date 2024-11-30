import os 

audio_dir = './raw_data/raw_audio_m4a'


for file in os.listdir(audio_dir):
    if file.endswith('.wav'):
        
        old_file_path = os.path.join(audio_dir, file)

        new_file_path = file[:-4] + '.m4a'

        new_file_path = os.path.join(audio_dir, new_file_path)

        os.rename(old_file_path, new_file_path)

print("Files renamed")        