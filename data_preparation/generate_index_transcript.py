import os 

transcript_path = "./raw_data/raw_transcript"

index = 761
end = 815

for i in range(index, end):

    txt_file_path = os.path.join(transcript_path, f"audio_sample_{i}.txt")

    with open(txt_file_path, 'w') as f:
        f.write('')

print("Empty Transcripts generated")        