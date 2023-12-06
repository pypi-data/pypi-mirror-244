# setup.py

from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'A lightweight and efficient JSON validation tool for Python.'
LONG_DESCRIPTION = """
JsonValidator is a Python package that provides an easy-to-use and robust solution for validating JSON data against a predefined schema. Designed to handle various data types and structures, including nested JSON objects, JsonValidator ensures your data adheres to the specified format and types, enhancing the reliability of your applications that process JSON data.

Features:
- Validates standard JSON data types including strings, numbers, objects, and lists.
- Supports custom validation for nested JSON structures.
- Provides clear, descriptive error messages for quick debugging.
- Easy integration into existing Python projects.

Ideal for:
- Data validation in web APIs.
- Ensuring data integrity in data processing pipelines.
- Rapid development in scenarios where JSON data structures are extensively used.

JsonValidator is simple yet powerful, making it an essential tool for any project that requires JSON data validation.
"""

# Setting up
setup(
    name="JSONEyeX",
    version=VERSION,
    author="venkata sidhartha (sidhu)",
    author_email="venkatasidhartha@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    package_dir={"":"JSONEyeX"},
    url="https://github.com/venkatasidhartha/JSONEyeX.git",
    packages=find_packages(where="JSONEyeX"),
    install_requires=['wheel'],
    keywords=['python', 'json-validator'],
)