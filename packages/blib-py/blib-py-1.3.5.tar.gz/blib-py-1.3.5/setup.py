from setuptools import setup, find_packages

from src.blib import __version__

with open("requirements.txt", "r") as fid:
    install_requires = [line.strip() for line in fid.readlines() if line.strip()]

print(install_requires)

with open("README.md", "r") as fid:
    long_description = fid.read()

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
    },
    include_package_data=True,
    license="MIT",
    zip_safe=False,
)
