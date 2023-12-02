import setuptools

from setuptools import find_packages


setuptools.setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
