import os
import subprocess

# Source Directory
source_path = "./Samrajya_Audio"

# Target Directory
target_path = "./raw_data/raw_audio_wav"

def Rename_Files():
    # Index to track file number(Change it according to current index)
    index = 815

    # Iteration through each file in the given directory
    for filename in os.listdir(source_path):
        
        # Constructing the old file path 
        # This is necessary because to perform any operations on the file (like renaming it, moving it, or reading from it)
        # you need the complete path to the file.
        # os.listdir(old_path) only gives the file name and not the path

        old_file_path = os.path.join(source_path, filename)

        if filename.lower().endswith('m4a'):

            # Renaming the files
            new_file_name = f"audio_sample_{index}.wav"
            # Constructing the new file path
            new_file_path = os.path.join(target_path, new_file_name)

            command = ['ffmpeg', '-i', old_file_path, new_file_path]

            try:
                subprocess.run(command, check=True)

                # Increasing the index
                index += 1

            except subprocess.CalledProcessError as e:
                print(f'Error converting {old_file_path}: {e}')



Rename_Files()

