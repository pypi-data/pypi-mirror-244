# Py4J - A walkthrough
This project is a simple implementation of [Py4J](https://www.py4j.org/index.html), a Python library that enables Python programs to dynamically access Java objects and methods. The goal of this project is to provide users with a guardrail to implement Py4J in their workflow.

[![Packaging Status](https://github.com/sagarlakshmipathy/Py4J/actions/workflows/python-publish.yml/badge.svg)](https://github.com/sagarlakshmipathy/Py4J/actions/workflows/python-publish.yml)
[![PyPi version](https://badgen.net/pypi/v/py4j-example/)](https://pypi.org/project/py4j-example/)
[![GitHub release](https://badgen.net/github/release/sagarlakshmipathy/Py4J)](https://github.com/sagarlakshmipathy/Py4J/releases/)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://github.com/sagarlakshmipathy/Py4J/blob/main/LICENSE)

## Getting Started
To get started with Py4J, you will need to have the below in your machine. 
* Java (Java 11 or above) - This project was tested with **Java 11**
* Add **JAVA_HOME** to your environment variables
* Python (Python 3.x) - This project was tested with **Python 3.10.11**
* Optional - Maven (only if you want to build from source) - This project's build was tested with **Maven 3.9.4**
You can find the installation instructions on their respective official websites.

Once you have Java and Python installed, you can proceed with the following steps:

* Install the package using pip `pip install py4j-example`

## Usage
* From your terminal, open python

    ```python```


* Run the below code which will let you use the underlying Java subtract method in python

```python
from py4j_example.app import ApplicationWrapper

wrapper = ApplicationWrapper()
result = wrapper.subtract(2, 1)

print(result)  # will output 1
```

* In addition to the subtract method, you can access other Java objects and methods (native and custom) from Python. 
For example, to call a Java method named `getArrayLength` that takes a list of integers as a parameter, you can do the following:

```python
from py4j_example.app import ApplicationWrapper

wrapper = ApplicationWrapper()
result = wrapper.getArrayLength([1, 2, 3])

print(result)  # will output 3
```
Note: Python doesn't have an equivalent data type for Java's `int[]`, so I've constructed a Java array from Python using Py4J. Refer to [this](https://github.com/sagarlakshmipathy/Py4J/blob/3fcda4718b837140317c889ef8c9bd86748bda2b/python/app.py#L30) code.

## Extending the application
You can extend the application by adding your own Java classes and methods.
* Create a new Java class in the `src/main/java/org/example/` directory or modify the existing `Application.java` class
* Add your custom methods to the class
* Add unit test cases for the Java methods in the `src/test/java/org/example/` directory
* Build the project using `mvn clean package`
* Modify the `pyhton/app.py` file to add your custom methods
* Add unit tests for your Python methods in the `python/tests/` directory
* Run the tests using `python -m pytest` from the project root directory

## Contributing
Contributions to this project are welcome. 
If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository.

