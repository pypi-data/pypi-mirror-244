from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="prnv",
    version="0.1",
    author="Masti Khor",
    description="A package for my friend.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/prnv",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "prnv=prnv.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)