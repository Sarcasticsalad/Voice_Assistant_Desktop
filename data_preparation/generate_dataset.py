import os
import pandas as pd
import re

# Define Directories
audio = './data/aligned_audio'
transcript = './data/aligned_transcript'

# Get list of audio and transcript files
audio_files =  sorted([file for file in os.listdir(audio) if file.endswith('.wav')],
                      key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))
transcript_files = sorted([file for file in os.listdir(transcript) if file.endswith('.txt')],
                          key=lambda x: int(re.search(r'(\d+)', x).group()) if re.search(r'(\d+)', x) else float('inf'))

# Ensure each list has same no of files
if len(audio_files) != len(transcript_files):
    raise ValueError('The length of audio files do not match the lenght of transcript files')

# Creating a Dictionary which consists of two keys that holds the location for all files
data =  {
           "audio_file" : [os.path.join(audio, file).replace('\\', '/') for file in audio_files],
           "transcript_file" : [os.path.join(transcript, file).replace('\\', '/') for file in transcript_files] 
        }

# Creating the DataFrame
df = pd.DataFrame(data)

# Converting DataFrame to CSV
df.to_csv("./data/metadata/aligned_data.csv", index=False)


