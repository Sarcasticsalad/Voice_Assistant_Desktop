import os

audio_path = "./raw_data/raw_audio"
transcript_path = "./raw_data/raw_transcript"


# Looping through each audio file to define a new transcript path with extension .txt

for file in os.listdir(audio_path):
    if file.endswith('.wav'):
        txt_file_path = os.path.join(transcript_path, file.replace('.wav', '.txt'))

    # Creating empty file with same name as audio file
    with open(txt_file_path, 'w') as f:
        f.write('')

print("Text files generated in transcript folder")