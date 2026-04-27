#!/usr/bin/env python
"""Unit tests for az_bicep_format function."""
import unittest
import sys
from unittest.mock import patch, MagicMock
from checkazurebiceppython import az_bicep_format


class TestAzBicepFormat(unittest.TestCase):
    """Test cases for az_bicep_format function."""

    @patch('checkazurebiceppython.subprocess.run')
    @patch('checkazurebiceppython.glob.glob')
    def test_bicep_format_no_files(self, mock_glob, mock_run):
        """Test bicep format when no bicep files are found."""
        mock_glob.return_value = []
        mock_run.return_value = MagicMock(stdout="Bicep CLI version 0.4.1008", stderr=b"")
        
        # Should not raise any exception when no files found
        az_bicep_format()
        
        # Verify version check was called
        mock_run.assert_any_call(
            ["az", "bicep", "version"], 
            stdout=unittest.mock.ANY, 
            text=True, 
            shell=True
        )

    @patch('checkazurebiceppython.subprocess.run')
    @patch('checkazurebiceppython.glob.glob')
    def test_bicep_format_successful(self, mock_glob, mock_run):
        """Test bicep format with successful formatting."""
        mock_glob.return_value = ['./test.bicep']
        
        # Mock version and format calls (no upgrade because --noupgrade is hardcoded)
        mock_run.side_effect = [
            MagicMock(stdout="Bicep CLI version 0.4.1008", stderr=b""),
            MagicMock(stdout=b"Format successful", stderr=b"")
        ]
        
        # Should complete without error
        az_bicep_format()
        
        # Verify format was called for the file
        self.assertEqual(mock_run.call_count, 2)

    @patch('checkazurebiceppython.subprocess.run')
    @patch('checkazurebiceppython.glob.glob')
    @patch('builtins.print')
    def test_bicep_format_with_errors(self, mock_print, mock_glob, mock_run):
        """Test bicep format with errors."""
        mock_glob.return_value = ['./test.bicep']
        
        # Mock version and failed format (no upgrade because --noupgrade is hardcoded)
        mock_run.side_effect = [
            MagicMock(stdout="Bicep CLI version 0.4.1008", stderr=b""),
            MagicMock(stdout=b"", stderr=b"Error: Invalid file")
        ]
        
        # Should exit with code 25
        with self.assertRaises(SystemExit) as cm:
            az_bicep_format()
        
        self.assertEqual(cm.exception.code, 25)

    @patch('checkazurebiceppython.subprocess.run')
    @patch('checkazurebiceppython.glob.glob')
    def test_bicep_format_multiple_files(self, mock_glob, mock_run):
        """Test bicep format with multiple files."""
        mock_glob.return_value = ['./test1.bicep', './test2.bicep']
        
        # Mock version and two successful formats (no upgrade because --noupgrade is hardcoded)
        mock_run.side_effect = [
            MagicMock(stdout="Bicep CLI version 0.4.1008", stderr=b""),
            MagicMock(stdout=b"Format successful", stderr=b""),
            MagicMock(stdout=b"Format successful", stderr=b"")
        ]
        
        # Should complete without error
        az_bicep_format()
        
        # Verify format was called for both files
        self.assertEqual(mock_run.call_count, 3)


if __name__ == '__main__':
    unittest.main()
