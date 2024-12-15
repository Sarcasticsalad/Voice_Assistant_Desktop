import os
import parselmouth
from pydub import AudioSegment
from parselmouth.praat import call


# Extract audio bits and create transcritps

def extract_audio_segments(audio_path, textgrid_path, output_audio_dir, output_transcript_dir):

    # Iterate through all audio files in the audio_path directory
    for file in os.listdir(audio_path):
        if file.endswith('.wav'):
            audio_file_path = os.path.join(audio_path, file)

            # Construct the corresponding textgrid file path
            textgrid_file = file.replace('.wav', '.TextGrid')
            textgrid_file_path = os.path.join(textgrid_path, textgrid_file)

            # Check if textgrid file exists
            if not os.path.isfile(textgrid_file_path):
                print(f"TextGrid file not found for {file}. Skipping")
                continue
    
            # Load audio file
            audio = AudioSegment.from_wav(audio_file_path)

            # Load TextGrid file
            textgrid = parselmouth.read(textgrid_file_path)

            # Locate the "words" tier by iterating over tiers
            words_tier = None
            num_tiers = call(textgrid, "Get number of tiers")
            for tier_index in range(1, num_tiers + 1):
                tier_name = call(textgrid, "Get tier name", tier_index)
                if tier_name == "words":
                    words_tier = tier_index
                    break

            if words_tier is None:
                print(f"No 'words' tier found in {textgrid_file}. Skipping")
                continue

            # Prepare to combine the audio segments and transcript text
            combined_audio = AudioSegment.empty()
            combined_transcript = ""

            # Process each interval in the "words" tier
            num_intervals = call(textgrid, "Get number of intervals", words_tier)
            for i in range(1, num_intervals + 1):
                xmin = call(textgrid, "Get start time of interval", words_tier, i)
                xmax = call(textgrid, "Get end time of interval", words_tier, i)
                text = call(textgrid, "Get label of interval", words_tier, i)

                # Skip empty intervals
                if text.strip() == "":
                    continue

                # Extract audio segment in milliseconds 
                segment = audio[int(xmin*1000):int(xmax*1000)]

                # Add the audio bits
                combined_audio += segment

                # Add the text bits
                combined_transcript += text + " "

            # Create base filename for output files
            base_filename = f"aligned_{file.split('.')[0]}"
                
            combined_audio.export(os.path.join(output_audio_dir, f"{base_filename}.wav"), format="wav")

            with open(os.path.join(output_transcript_dir, f"{base_filename}.txt"), 'w') as f:
                f.write(combined_transcript.strip())

    print("Extraction Complete")


audio_path = './raw_data/raw_audio_16k'
textgrid_path = './raw_data/textgrid'
output_audio_dir = './data/aligned_audio'
output_transcript_dir = './data/aligned_transcript'

extract_audio_segments(audio_path, textgrid_path, output_audio_dir, output_transcript_dir)