import os
import sys
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(this_directory, 'py4j_example/version.py')

try:
    exec(open(version_file).read())
except IOError:
    print(f"Failed to load version file for packaging. {version_file} not found!", file=sys.stderr)
    sys.exit(-1)
VERSION = __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py4j-example",
    version=VERSION,
    packages=find_packages(),
    package_data={"py4j_example": ["jars/*.jar"]},  # Include JAR files in the package
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
