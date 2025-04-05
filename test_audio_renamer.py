#!/usr/bin/env python3
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys

# Add the parent directory to the path so we can import the main script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audio_file_renamer import (
    parse_filename,
    pitch_to_numeric,
    numeric_to_pitch,
    decrease_pitch_by_semitone,
    translate_velocity,
)


class TestAudioFileRenamer(unittest.TestCase):
    def test_parse_filename(self):
        """Test parsing filenames with various formats."""
        test_cases = [
            {
                "filename": "/path/to/Piano - Soft-C3-V42-3GUZ.wav",
                "expected": {
                    "sound_name": "Piano - Soft",
                    "starting_pitch": "C3",
                    "velocity": 42,
                    "code": "3GUZ",
                    "file_path": "/path/to/Piano - Soft-C3-V42-3GUZ.wav",
                    "extension": "wav",
                },
            },
            {
                "filename": "/path/to/Violin-A#4-V127-ABCD.aif",
                "expected": {
                    "sound_name": "Violin",
                    "starting_pitch": "A#4",
                    "velocity": 127,
                    "code": "ABCD",
                    "file_path": "/path/to/Violin-A#4-V127-ABCD.aif",
                    "extension": "aif",
                },
            },
            {
                "filename": "/path/to/Bass Drum-G1-V01-XYZ1.wav",
                "expected": {
                    "sound_name": "Bass Drum",
                    "starting_pitch": "G1",
                    "velocity": 1,
                    "code": "XYZ1",
                    "file_path": "/path/to/Bass Drum-G1-V01-XYZ1.wav",
                    "extension": "wav",
                },
            },
        ]

        for tc in test_cases:
            with self.subTest(filename=tc["filename"]):
                result = parse_filename(tc["filename"])
                self.assertEqual(result, tc["expected"])

    def test_invalid_filename_returns_none(self):
        """Test that invalid filenames return None instead of raising errors."""
        invalid_filenames = [
            "/path/to/Piano.wav",  # Missing pitch, velocity, and code
            "/path/to/Piano-C3-missing.wav",  # Missing velocity and code
            "/path/to/Piano-C3-V42.wav",  # Missing code
            "/path/to/Piano-H3-V42-ABCD.wav",  # Invalid note name (H)
            "/path/to/Piano-C-V42-ABCD.wav",  # Missing octave number
            "/path/to/Piano-C3-V4X-ABCD.wav",  # Non-numeric velocity
            "/path/to/Piano-C3-V42-AB.wav",  # Code too short
        ]

        for filename in invalid_filenames:
            with self.subTest(filename=filename):
                result = parse_filename(filename)
                self.assertIsNone(
                    result, f"Expected None for invalid filename: {filename}"
                )

    def test_pitch_to_numeric(self):
        """Test conversion of pitch notation to numeric values."""
        test_cases = [
            {"pitch": "C0", "expected": 0},
            {"pitch": "C#0", "expected": 1},
            {"pitch": "D0", "expected": 2},
            {"pitch": "C1", "expected": 12},
            {"pitch": "A4", "expected": 57},  # Middle A (A440)
            {"pitch": "C8", "expected": 96},  # Highest C on piano
        ]

        for tc in test_cases:
            with self.subTest(pitch=tc["pitch"]):
                result = pitch_to_numeric(tc["pitch"])
                self.assertEqual(result, tc["expected"])

    def test_numeric_to_pitch(self):
        """Test conversion of numeric values back to pitch notation."""
        test_cases = [
            {"numeric": 0, "expected": "C0"},
            {"numeric": 1, "expected": "C#0"},
            {"numeric": 2, "expected": "D0"},
            {"numeric": 12, "expected": "C1"},
            {"numeric": 57, "expected": "A4"},  # Middle A (A440)
            {"numeric": 96, "expected": "C8"},  # Highest C on piano
        ]

        for tc in test_cases:
            with self.subTest(numeric=tc["numeric"]):
                result = numeric_to_pitch(tc["numeric"])
                self.assertEqual(result, tc["expected"])

    def test_decrease_pitch_by_semitone(self):
        """Test decreasing a pitch by one semitone."""
        test_cases = [
            {"pitch": "C1", "expected": "B0"},  # Test octave change
            {"pitch": "C#1", "expected": "C1"},
            {"pitch": "A4", "expected": "G#4"},
            {"pitch": "F#2", "expected": "F2"},
        ]

        for tc in test_cases:
            with self.subTest(pitch=tc["pitch"]):
                result = decrease_pitch_by_semitone(tc["pitch"])
                self.assertEqual(result, tc["expected"])

    def test_translate_velocity(self):
        """Test translation of velocity values to dynamic markings."""
        test_cases = [
            {"velocity": 0, "expected": "ppp"},
            {"velocity": 18, "expected": "ppp"},
            {"velocity": 19, "expected": "pp"},
            {"velocity": 36, "expected": "pp"},
            {"velocity": 37, "expected": "p"},
            {"velocity": 54, "expected": "p"},
            {"velocity": 55, "expected": "mf"},
            {"velocity": 72, "expected": "mf"},
            {"velocity": 73, "expected": "f"},
            {"velocity": 90, "expected": "f"},
            {"velocity": 91, "expected": "ff"},
            {"velocity": 108, "expected": "ff"},
            {"velocity": 109, "expected": "fff"},
            {"velocity": 127, "expected": "fff"},
        ]

        for tc in test_cases:
            with self.subTest(velocity=tc["velocity"]):
                result = translate_velocity(tc["velocity"])
                self.assertEqual(result, tc["expected"])


class TestIntegration(unittest.TestCase):
    @patch("os.rename")
    @patch("glob.glob")
    def test_process_files(self, mock_glob, mock_rename):
        """Integration test for processing multiple files."""
        # Create test file paths that glob would return
        test_files = [
            "/test/Piano-C1-V32-ABCD.wav",
            "/test/Piano-C2-V32-ABCD.wav",
            "/test/Piano-C3-V64-ABCD.wav",
            "/test/Piano-C4-V96-ABCD.wav",
            "/test/Drum-A1-V127-XYZW.wav",
            "/test/Drum-A2-V127-XYZW.wav",
            "/test/Synth-F#3-V10-1234.aif",
            "/test/Synth-G#3-V10-1234.aif",
        ]
        mock_glob.side_effect = lambda path, recursive: (
            test_files if ".wav" in path or ".aif" in path else []
        )

        # Import the main module function
        from audio_file_renamer import process_audio_files

        # Run the process
        with patch("builtins.print") as mock_print:
            process_audio_files("/test")

        # Expected renames with new format: {prog}{soundname}_{translated_velocity}_{starting pitch}.{extension}
        expected_renames = [
            # Piano group (sorted by pitch)
            ("/test/Piano-C1-V32-ABCD.wav", "/test/001Piano_p_C1.wav"),
            ("/test/Piano-C2-V32-ABCD.wav", "/test/002Piano_p_C2.wav"),
            ("/test/Piano-C3-V64-ABCD.wav", "/test/003Piano_mf_C3.wav"),
            ("/test/Piano-C4-V96-ABCD.wav", "/test/004Piano_f_C4.wav"),
            # Drum group (sorted by pitch)
            ("/test/Drum-A1-V127-XYZW.wav", "/test/001Drum_fff_A1.wav"),
            ("/test/Drum-A2-V127-XYZW.wav", "/test/002Drum_fff_A2.wav"),
            # Synth group (sorted by pitch, sharp signs removed)
            ("/test/Synth-F#3-V10-1234.aif", "/test/001Synth_ppp_F3.aif"),
            ("/test/Synth-G#3-V10-1234.aif", "/test/002Synth_ppp_G3.aif"),
        ]

        # Check that os.rename was called with the correct arguments
        self.assertEqual(mock_rename.call_count, len(test_files))
        rename_calls = [call[0] for call in mock_rename.call_args_list]

        for (source, target), (exp_source, exp_target) in zip(
            rename_calls, expected_renames
        ):
            self.assertEqual(source, exp_source)
            self.assertEqual(target, exp_target)

    @patch("os.rename")
    @patch("glob.glob")
    def test_process_files_skips_invalid_filenames(self, mock_glob, mock_rename):
        """Test that files with invalid names are skipped during processing."""
        # Mix of valid and invalid files
        test_files = [
            "/test/Piano-C1-V32-ABCD.wav",  # Valid
            "/test/Piano-C2-V32-ABCD.wav",  # Valid
            "/test/InvalidName.wav",  # Invalid - doesn't match pattern
            "/test/Piano-X3-V64-ABCD.wav",  # Invalid - invalid note name
            "/test/Drum-A1-V127-XYZW.wav",  # Valid
            "/test/Piano-C4-missing.wav",  # Invalid - incomplete format
        ]

        mock_glob.side_effect = lambda path, recursive: (
            test_files if ".wav" in path or ".aif" in path else []
        )

        # Import the main module function
        from audio_file_renamer import process_audio_files

        # Run the process
        with patch("builtins.print") as mock_print:
            process_audio_files("/test")

        # Expected renames (only valid files) with new format
        expected_renames = [
            ("/test/Piano-C1-V32-ABCD.wav", "/test/001Piano_p_C1.wav"),
            ("/test/Piano-C2-V32-ABCD.wav", "/test/002Piano_p_C2.wav"),
            ("/test/Drum-A1-V127-XYZW.wav", "/test/001Drum_fff_A1.wav"),
        ]

        # Check that only valid files were renamed
        self.assertEqual(mock_rename.call_count, len(expected_renames))

        # Get all the rename calls
        rename_calls = [call[0] for call in mock_rename.call_args_list]

        # Check each call matches our expected calls
        for (source, target), (exp_source, exp_target) in zip(
            rename_calls, expected_renames
        ):
            self.assertEqual(source, exp_source)
            self.assertEqual(target, exp_target)

        # Verify that we printed messages about skipping invalid files
        skipped_message_calls = [
            call
            for call in mock_print.call_args_list
            if "Skipping file with invalid format:" in str(call)
        ]
        self.assertEqual(len(skipped_message_calls), 3)  # Three invalid files

    @patch("os.rename")
    @patch("glob.glob")
    def test_process_files_removes_spaces(self, mock_glob, mock_rename):
        """Test that spaces are removed from sound names in the output filenames."""
        # Test files with spaces in sound names
        test_files = [
            "/test/Piano with Space-C1-V32-ABCD.wav",
            "/test/Grand Piano-C2-V64-ABCD.wav",
            "/test/Multiple   Spaces-G3-V96-XYZW.wav",
            "/test/No Space-A4-V127-1234.aif",
        ]

        mock_glob.side_effect = lambda path, recursive: (
            test_files if ".wav" in path or ".aif" in path else []
        )

        # Import the main module function
        from audio_file_renamer import process_audio_files

        # Run the process
        with patch("builtins.print") as mock_print:
            process_audio_files("/test")

        # Expected renames with spaces removed from sound names and new format
        expected_renames = [
            (
                "/test/Piano with Space-C1-V32-ABCD.wav",
                "/test/001PianowithSpace_p_C1.wav",
            ),
            ("/test/Grand Piano-C2-V64-ABCD.wav", "/test/001GrandPiano_mf_C2.wav"),
            (
                "/test/Multiple   Spaces-G3-V96-XYZW.wav",
                "/test/001MultipleSpaces_f_G3.wav",
            ),
            ("/test/No Space-A4-V127-1234.aif", "/test/001NoSpace_fff_A4.aif"),
        ]

        # Check that os.rename was called with the correct arguments
        self.assertEqual(mock_rename.call_count, len(test_files))
        rename_calls = [call[0] for call in mock_rename.call_args_list]

        for (source, target), (exp_source, exp_target) in zip(
            rename_calls, expected_renames
        ):
            self.assertEqual(source, exp_source)
            self.assertEqual(target, exp_target)


if __name__ == "__main__":
    unittest.main()
