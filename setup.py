# Standard library imports
import pathlib

# Third party imports
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="outlier_analysis", 
    version="0.0.1",
    author="Erin Gill",
    author_email="erin.gill81@gmail.com",
    description="Methods to automatically parse longitudinal numeric data for outliers using IQR and modified z-score, will also predict future time points using linear regression",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eringill/outlier_analysis",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL 3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'copy', 'matplotlib', 'plotnine', 'warnings', 'scipy', 'statistics', 'pandas', 'sklearn'],

)