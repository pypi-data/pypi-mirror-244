#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from pathlib import Path

with open("README.md") as readme_file:
    readme = readme_file.read()

# Get the path to the requirements.txt file
requirements_path = Path(__file__).parent / 'requirements.txt'

# Read the contents of the requirements file
with open(requirements_path) as f:
    requirements = f.read().splitlines()

test_requirements = [
    "pytest>=3",
]

setup(
    author="Jack Tierney",
    author_email="jackcurragh@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A python command-line utility for working with RiboSeq.Orgs Data Portal",
    entry_points={
        "console_scripts": [
            "RDP-Tools=RDPTools.RDPTools:rdp_tools",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords="RDP-Tools",
    name="RiboSeq-DP-Tools",
    packages=find_packages(
        include=["RDPTools", "RDPTools.*"],
        exclude=[
            "sample_data/*",
        ],
    ),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/riboseqorg/RDP-Tools",
    version="0.1.4",
    zip_safe=False,
)
