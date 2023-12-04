from setuptools import setup, find_packages

from src.blib import __version__

install_requires = ["numpy", "matplotlib"]

# Setup
setup(
    name="blib-py",
    version=__version__,
    description="For convenient coding",
    author="Boonleng Cheong",
    author_email="boonleng@ou.edu",
    url="https://github.com/boonleng/blib-py",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "blib.fonts": ["*.ttf"],
    },
    include_package_data=True,
    license="MIT",
    install_requires=install_requires,
    zip_safe=False,
)
