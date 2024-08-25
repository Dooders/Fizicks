# setup.py
from setuptools import setup, find_packages

setup(
    name="fizicks",
    version="0.2.2",
    author="Chris Mangum",
    author_email="csmangum@gmail.com",
    description="A state-driven physics model designed to simulate cause and effect within a physical space.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/fizicks/",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
