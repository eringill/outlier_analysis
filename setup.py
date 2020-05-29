import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="outliers-egill", 
    version="0.0.1",
    author="Erin Gill",
    author_email="erin.gill81@gmail.com",
    description="Methods to automatically parse longitudinal numeric data for outliers using IQR and modified z-score, will also predict future time points using linear regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egill/Outlier_analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL 3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)