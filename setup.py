from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Anomalyze",
    version="1.0.0",
    author="Mikhail Nazarenko",
    author_email="mikhail.nazarenko@gmail.com",
    description="A comprehensive anomaly detection system for real-time data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/anomalyze",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.2",
        "scipy>=1.5.2",
        "statsmodels>=0.12.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
