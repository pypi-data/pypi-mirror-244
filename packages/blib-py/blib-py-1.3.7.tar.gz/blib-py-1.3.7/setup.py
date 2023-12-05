from setuptools import setup, find_packages

from src.blib import __version__

with open("requirements.txt", "r") as fh:
    install_requires = [line.strip() for line in fh.readlines() if line.strip()]

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setup
setup(
    name="blib-py",
    version=__version__,
    description="Boonleng's Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Boonleng Cheong",
    author_email="boonleng@ou.edu",
    url="https://github.com/boonleng/blib-py",
    install_requires=install_requires,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "blib.fonts": ["*.ttf"],
        "blib.blob": ["line-*.png"],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
)
