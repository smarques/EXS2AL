# EXS2AL

A Python utility for renaming audio sample files created by Apple Autosampler EXS format so they can be imported into IOS AudioLayer sampler.
Note: when you configure Autosampler it might be better to choose only white key root notes, I noticed some errors when importing file names that have a sharp (#) sign.

## File Naming Conventions

### Input Format

Files created by Autosampler will have the format:

```
{sound_name}-{root_pitch}-V{velocity}-{4_letter_code}.{extension}
```

Example: `Piano-C3-V64-ABCD.wav`

Where:

- `sound_name`: The name of the instrument/sound (can include spaces)
- `root_pitch`: Musical pitch notation (e.g., C3, F#4)
- `velocity`: MIDI velocity value (0-127) prefixed with 'V'
- `4_letter_code`: Four character identifier
- `extension`: Audio file extension (wav, aif, etc.)

**Note**: Files that do not match this naming pattern will be skipped during processing, with a message printed to the console.

### Output Format

```
{prog}{soundname}_{translated_velocity}_{starting pitch}.{extension}
```

Example: `001Piano_mf_C3.wav`

Where:

- `prog`: Progressive index (3 digits, padded with zeros) for ordering files
- `soundname`: Preserved from input but with spaces removed for better file compatibility
- `translated_velocity`: Musical dynamic marking translated from velocity value
- `root_pitch`: Preserved from input (sharp signs are removed)
- `extension`: Audio file extension

Files are sorted by:

1. Starting pitch (ascending)
2. Velocity (ascending)

## Installation

No installation is required beyond Python 3.6 or higher.

## Usage

```bash
python audio_file_renamer.py <folder_path>
```

Where `<folder_path>` is the path to the directory containing audio files to rename.

## How It Works

1. **File Discovery**: Recursively finds all .wav, .aif, and .aiff files in the specified directory
2. **Filename Parsing**: Extracts sound name, starting pitch, velocity, and code using regex
   - Files not matching the expected pattern are skipped with a warning message
3. **Group Organization**: Groups files by sound name and sorts by pitch and velocity
4. **Velocity Translation**: Maps MIDI velocity values (0-127) to musical dynamics:
   - ppp (pianississimo): 0-18
   - pp (pianissimo): 19-36
   - p (piano): 37-54
   - mf (mezzo-forte): 55-72
   - f (forte): 73-90
   - ff (fortissimo): 91-108
   - fff (fortississimo): 109-127
5. **File Renaming**:
   - Removes spaces from the sound name for better compatibility
   - Removes sharp signs from starting pitch
   - Adds progressive index for ordering
   - Renames each file with the format: {prog}{soundname}_{dynamics}_{pitch}.{extension}
6. **Summary Output**: Displays the number of files processed and skipped

## Testing

This project includes several test components:

### Unit Tests

Run the unit tests with:

```bash
python test_audio_renamer.py
```

### Creating Test Files

To create sample files for testing:

#### On Linux/macOS:

```bash
chmod +x create_test_files.sh
./create_test_files.sh
```

#### On Windows:

```powershell
.\create_test_files.ps1
```

This will create a directory named `test_audio_files` with empty audio files named according to the input format.

### Expected Output

The `expected_output.txt` file contains the expected results after renaming, which you can use to verify the script's operation.

## Examples

### Before Renaming

```
Piano-C1-V32-ABCD.wav
Piano-C2-V32-ABCD.wav
Piano-C3-V64-ABCD.wav
Violin-A#4-V127-DEFG.aif
Grand Piano-C2-V64-ABCD.wav
Uomini Di Abissi - grattuggia-C1-V42-3GUZ.wav
invalid_file.wav  # This will be skipped
```

### After Renaming

```
001Piano_p_C1.wav
002Piano_p_C2.wav
003Piano_mf_C3.wav
001Violin_fff_A4.aif
001GrandPiano_mf_C2.wav
001UominiDiAbissi-grattuggia_p_C1.wav
invalid_file.wav  # Unchanged as it doesn't match the pattern
```

## Technical Details

- **Pitch Conversion**: Converts between pitch notation (C4, F#2, etc.) and numeric values for comparison
- **Dynamic Calculation**: Divides the MIDI velocity range (0-127) into 7 segments for dynamic markings
- **Error Handling**: Files with invalid naming patterns are skipped rather than causing errors
- **Name Sanitization**: Spaces are removed from sound names for better cross-platform compatibility
- **Sorting**: Files are sorted by pitch and velocity within each sound group
- **Progressive Index**: Each file gets a 3-digit index for ordering

## License

This project is available under the MIT License.

## Contributing

Contributions, bug reports, and feature requests are welcome!
