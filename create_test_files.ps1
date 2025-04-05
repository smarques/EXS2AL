# PowerShell script to create empty audio files for testing the audio_file_renamer.py script

# Create a test directory
New-Item -ItemType Directory -Force -Path "test_audio_files"
Set-Location -Path "test_audio_files"

# Piano samples
New-Item -ItemType File -Force -Path "Piano-C1-V32-ABCD.wav"
New-Item -ItemType File -Force -Path "Piano-C2-V32-ABCD.wav"
New-Item -ItemType File -Force -Path "Piano-C3-V64-ABCD.wav"
New-Item -ItemType File -Force -Path "Piano-C4-V96-ABCD.wav"
New-Item -ItemType File -Force -Path "Piano-C5-V110-ABCD.wav"
New-Item -ItemType File -Force -Path "Piano-G6-V127-ABCD.wav"

# Violin samples
New-Item -ItemType File -Force -Path "Violin-A3-V10-DEFG.wav"
New-Item -ItemType File -Force -Path "Violin-A#3-V42-DEFG.wav"
New-Item -ItemType File -Force -Path "Violin-B3-V85-DEFG.wav"
New-Item -ItemType File -Force -Path "Violin-C4-V127-DEFG.wav"
New-Item -ItemType File -Force -Path "Violin-C#4-V110-DEFG.wav"
New-Item -ItemType File -Force -Path "Violin-D4-V90-DEFG.wav"

# Drum kit samples
New-Item -ItemType File -Force -Path "Kick Drum-C1-V80-DRUM.wav"
New-Item -ItemType File -Force -Path "Snare-D1-V90-DRUM.wav"
New-Item -ItemType File -Force -Path "Hi-Hat-F#1-V70-DRUM.wav"
New-Item -ItemType File -Force -Path "Crash Cymbal-A2-V100-DRUM.wav"

# Complex sample names
New-Item -ItemType File -Force -Path "Uomini Di Abissi - grattuggia-C1-V42-3GUZ.wav"
New-Item -ItemType File -Force -Path "Uomini Di Abissi - grattuggia-D1-V84-3GUZ.wav"
New-Item -ItemType File -Force -Path "Uomini Di Abissi - grattuggia-E1-V127-3GUZ.wav"

Write-Host "Created empty test files in .\test_audio_files\"
Write-Host "Run the audio_file_renamer.py script on this directory to test:"
Write-Host "python audio_file_renamer.py test_audio_files" 