from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent

setup(
    name="inputselect",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "keyboard>=0.6.0"
    ],
    author="ItchyPython3759",
    description="A Python module for selecting options in the Python interactive terminal.",
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type="text/markdown"
)
