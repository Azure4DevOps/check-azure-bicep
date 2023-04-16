import unittest
import subprocess
from unittest.mock import patch

class TestBicepBuild(unittest.TestCase):

    def test_bicep_build(self):

        # mock the subprocess.run() function to return a version and upgrade output
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [
                subprocess.CompletedProcess(['az', 'bicep', 'version'], stdout=b"1.0.0\n", stderr=""),
                subprocess.CompletedProcess(['az', 'bicep', 'upgrade'], stdout=b"Upgrading Bicep CLI version 0.4.100 to 1.0.0\n", stderr="")
            ]

            # mock the glob.glob() function to return a list of bicep files
            with patch('glob.glob', return_value=['./path/to/example.bicep']):
                # run the code being tested
                result = subprocess.run(["python", "test.py"], shell=True, capture_output=True)

                # assert that the subprocess.run() function was called with the correct arguments
                mock_run.assert_any_call(['az', 'bicep', 'version'], stdout=subprocess.PIPE, text=True, shell=True)
                mock_run.assert_any_call(['az', 'bicep', 'upgrade'], stdout=subprocess.PIPE, text=True, shell=True)
                mock_run.assert_any_call(['az', 'bicep', 'build', '--stdout', '--file', './path/to/example.bicep'], shell=True, capture_output=True)

                # assert that the output is as expected
                self.assertEqual(result.returncode, 0, "Expected return code 0")
                self.assertEqual(result.stderr, b"", "Expected empty stderr")
