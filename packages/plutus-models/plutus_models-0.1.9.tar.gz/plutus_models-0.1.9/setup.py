from setuptools import setup, find_packages

setup(
    name="plutus_models",
    version="0.1.9",
    description="models for plutus app",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
