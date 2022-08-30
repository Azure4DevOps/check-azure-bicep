import setuptools
import glob
import subprocess
import sys

def get_project_requirements() -> str:
    with open(f"requirements.txt", "r") as f:
        return f.read()
    
def my_function2():

  biceps_version = subprocess.run(["az", "bicep", "version"], stdout=subprocess.PIPE, text=True, shell=True)
  biceps_version = subprocess.run(["az", "bicep", "upgrade"], stdout=subprocess.PIPE, text=True, shell=True)
  #print(biceps_version.stdout)

  #print(glob.glob("./**/*.bicep", recursive=True))
  any_error = None
  for bicep_file in glob.glob("./**/*.bicep", recursive=True):
      result = subprocess.run(["az", "bicep", "build", "--stdout", "--file", bicep_file], shell=True, capture_output=True)

      if result.stderr:
          print(result.stderr)
          any_error = True

  if any_error:
      sys.exit(25)
        
setuptools.setup(
    name="check-azure-bicep-python",
    description="check-azure-bicep-python",
    long_description_content_type="text/markdown",
    url="https://github.com/Azure4DevOps/check-azure-bicep",
    python_requires="==3.10.*",
    license="MIT",
    packages=setuptools.find_packages(
        include=["*"],
    ),
    install_requires=get_project_requirements(),
    entry_points={
        "console_scripts": [
        "my_function=checkazurebiceppython:my_function2",
        ]
    },
)
