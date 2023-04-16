import unittest
import subprocess
import os

class TestBicepBuild(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create a test directory and change to it
        os.mkdir("test_dir")
        os.chdir("test_dir")

        # create some test bicep files
        with open("main.bicep", "w") as f:
            f.write('resource test_resource "Microsoft.Storage/storageAccounts@2021-04-01" = {\n  name: "test"\n  location: "eastus"\n  sku: {\n    name: "Standard_LRS"\n  }\n}')

        with open("module/module.bicep", "w") as f:
            f.write('module test_module "./../module"\n')

        with open("module/module.json", "w") as f:
            f.write('{\n  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",\n  "contentVersion": "1.0.0.0",\n  "resources": []\n}')

    @classmethod
    def tearDownClass(cls):
        # change back to the original directory and remove the test directory
        os.chdir("..")
        os.rmdir("test_dir")

    def test_bicep_build(self):
        # run the bicep build command
        result = subprocess.run(["python", "test.py"], shell=True, capture_output=True)

        # assert that the output is as expected
        self.assertEqual(result.returncode, 0, "Expected return code 0")
        self.assertEqual(result.stderr, b"", "Expected empty stderr")
        self.assertIn(b"Resource 'test_resource' was built successfully.", result.stdout)
        self.assertIn(b"module.json: Finished successfully", result.stdout)
