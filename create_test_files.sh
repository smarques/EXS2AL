#!/bin/bash
# Script to create empty audio files for testing the audio_file_renamer.py script

# Create a test directory
mkdir -p test_audio_files
cd test_audio_files

# Piano samples
touch "Piano-C1-V32-ABCD.wav"
touch "Piano-C2-V32-ABCD.wav"
touch "Piano-C3-V64-ABCD.wav"
touch "Piano-C4-V96-ABCD.wav"
touch "Piano-C5-V110-ABCD.wav"
touch "Piano-G6-V127-ABCD.wav"

# Violin samples
touch "Violin-A3-V10-DEFG.wav"
touch "Violin-A#3-V42-DEFG.wav"
touch "Violin-B3-V85-DEFG.wav"
touch "Violin-C4-V127-DEFG.wav"
touch "Violin-C#4-V110-DEFG.wav"
touch "Violin-D4-V90-DEFG.wav"

# Drum kit samples
touch "Kick Drum-C1-V80-DRUM.wav"
touch "Snare-D1-V90-DRUM.wav"
touch "Hi-Hat-F#1-V70-DRUM.wav"
touch "Crash Cymbal-A2-V100-DRUM.wav"

# Complex sample names
touch "Uomini Di Abissi - grattuggia-C1-V42-3GUZ.wav"
touch "Uomini Di Abissi - grattuggia-D1-V84-3GUZ.wav"
touch "Uomini Di Abissi - grattuggia-E1-V127-3GUZ.wav"

echo "Created empty test files in ./test_audio_files/"
echo "Run the audio_file_renamer.py script on this directory to test:"
echo "python3 audio_file_renamer.py test_audio_files" 