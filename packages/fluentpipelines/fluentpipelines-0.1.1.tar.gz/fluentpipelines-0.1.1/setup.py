from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fluentpipelines",
    version="0.1.1",
    author="Jarriq Rolle",
    author_email="jrolle@bnbbahamas.com",
    description="A Python package for building fluent pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JarriqTheTechie/fluentpipelines",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)