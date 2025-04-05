#!/usr/bin/env python3
import os
import re
import glob
import sys
from collections import defaultdict


def parse_filename(filename):
    """
    Parse a filename to extract sound name, starting pitch, velocity, and code.
    Example: "Uomini Di Abissi - grattuggia-C1-V42-3GUZ.wav"

    Returns a dictionary with extracted components or None if the filename doesn't match the pattern.
    """
    # Get base name without extension
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Extract components using regex
    # Format: {sound_name}-{pitch}-V{velocity}-{code}
    pattern = r"(.*)-([A-G][#]?\d+)-V(\d+)-([A-Z0-9]{4})$"
    match = re.match(pattern, base_name)

    if not match:
        # Return None instead of raising an error for files that don't match the pattern
        return None

    sound_name, pitch, velocity, code = match.groups()
    return {
        "sound_name": sound_name.strip(),
        "starting_pitch": pitch,
        "velocity": int(velocity),
        "code": code,
        "file_path": filename,
        "extension": os.path.splitext(filename)[1][1:],  # Extension without dot
    }


def pitch_to_numeric(pitch):
    """
    Convert pitch notation (e.g., "C1", "F#4") to a numeric value for comparison.
    """
    # Map of note names to semitone values within an octave
    note_values = {
        "C": 0,
        "C#": 1,
        "D": 2,
        "D#": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "G": 7,
        "G#": 8,
        "A": 9,
        "A#": 10,
        "B": 11,
    }

    # Extract note and octave
    if "#" in pitch:
        note = pitch[:2]
        octave = int(pitch[2:])
    else:
        note = pitch[0]
        octave = int(pitch[1:])

    # Calculate numeric value (octave * 12 + note value)
    return (octave * 12) + note_values.get(note, 0)


def numeric_to_pitch(numeric_value):
    """
    Convert a numeric pitch value back to pitch notation.
    """
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = numeric_value // 12
    note_index = numeric_value % 12
    return f"{notes[note_index]}{octave}"


def decrease_pitch_by_semitone(pitch):
    """
    Decrease a pitch by one semitone.
    """
    numeric = pitch_to_numeric(pitch)
    return numeric_to_pitch(numeric - 1)


def translate_velocity(velocity):
    """
    Translate a velocity value (0-127) to a dynamic marking.
    """
    dynamic_markings = ["ppp", "pp", "p", "mf", "f", "ff", "fff"]

    # Map velocity to a segment index (0-6)
    segment_size = 128 // len(dynamic_markings)
    index = min(velocity // segment_size, len(dynamic_markings) - 1)

    return dynamic_markings[index]


def sanitize_sound_name(sound_name):
    """
    Sanitize the sound name by removing spaces, dashes, and underscores.
    """
    # Remove spaces, dashes, and underscores
    return sound_name.replace(" ", "").replace("-", "").replace("_", "")


def process_audio_files(folder_path):
    """
    Process all audio files in the given folder.
    """
    # Find all audio files
    audio_extensions = [".wav", ".aif", ".aiff"]
    audio_files = []

    for ext in audio_extensions:
        audio_files.extend(
            glob.glob(os.path.join(folder_path, f"**/*{ext}"), recursive=True)
        )

    if not audio_files:
        print(f"No audio files found in {folder_path}")
        return

    # Parse filenames and group by sound name
    sound_groups = defaultdict(list)
    parsed_files = []
    skipped_files = []

    for file_path in audio_files:
        parsed = parse_filename(file_path)
        if parsed is None:
            # Skip files that don't match the expected pattern
            skipped_files.append(file_path)
            print(f"Skipping file with invalid format: {os.path.basename(file_path)}")
            continue

        parsed_files.append(parsed)
        sound_groups[parsed["sound_name"]].append(parsed)

    if skipped_files:
        print(
            f"Skipped {len(skipped_files)} files that didn't match the expected naming pattern."
        )

    if not parsed_files:
        print("No valid audio files found with the expected naming pattern.")
        return

    # Process each sound group
    for sound_name, files in sound_groups.items():
        # Sort files by pitch and velocity
        files.sort(key=lambda x: (pitch_to_numeric(x["starting_pitch"]), x["velocity"]))

        # Process each file to determine new filename
        for index, parsed in enumerate(files, start=1):
            # Remove sharp signs from starting pitch
            starting_pitch = parsed["starting_pitch"].replace("#", "")

            # Translate velocity
            translated_velocity = translate_velocity(parsed["velocity"])

            # Create new filename - Sanitize sound name and use new format
            sanitized_sound_name = sanitize_sound_name(sound_name)
            # New format: {prog}{soundname}_{translated_velocity}_{starting pitch}.{extension}
            new_filename = f"{index:03d}{sanitized_sound_name}_{translated_velocity}_{starting_pitch}.{parsed['extension']}"
            new_filepath = os.path.join(
                os.path.dirname(parsed["file_path"]), new_filename
            )

            # Rename the file
            print(
                f"Renaming:\n  {os.path.basename(parsed['file_path'])}\n  to: {new_filename}"
            )
            os.rename(parsed["file_path"], new_filepath)

    print(f"Successfully renamed {len(parsed_files)} files.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python audio_file_renamer.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        sys.exit(1)

    try:
        process_audio_files(folder_path)
        print("Audio file renaming completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
