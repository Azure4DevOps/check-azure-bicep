import setuptools

def get_project_requirements() -> str:
    with open(f"requirements.txt", "r") as f:
        return f.read()

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
)
