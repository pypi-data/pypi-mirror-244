# Python Requisites

Python Requisites is a dynamic tool for the explicit declaration and analysis of dependencies in Python objects, streamlining the process of identifying and managing required elements in your code.

## Introduction

Python Requisites (or `python-requisites`) provides an intuitive way to analyze and declare the dependencies in Python objects like functions, classes, and modules. This tool is particularly useful for developers looking to gain better insight into their code's structure and dependencies.

## Features

- **Explicit Dependency Declaration**: Clearly outlines the dependencies within Python objects.
- **Streamlined Analysis**: Simplifies the process of identifying required arguments and dependencies in functions, classes, and modules.
- **Easy Integration**: Designed to seamlessly integrate with existing Python projects.

## Installation

You can install Python Requisites using pip:

```bash
pip install python-requisites
```

## Usage

This library provides a utility to collect function parameters dynamically, either as positional or keyword arguments. Below are examples demonstrating how to use this functionality:

### Collecting Positional or Keyword Arguments

```python
from requisites import collect_params

def sample_function(argument):
    return argument

# Example 1: Collecting positional arguments
args, kwargs = collect_params(sample_function, "hello")
# args will be ("hello",)
# kwargs will be {}
assert sample_function(*args, **kwargs) == "hello"

# Example 2: Collecting keyword arguments
args, kwargs = collect_params(sample_function, argument="hello")
# args will be ()
# kwargs will be {"argument": "hello"}
assert sample_function(*args, **kwargs) == "hello"

# Example 3: Combining positional and keyword arguments
args, kwargs = collect_params(sample_function, "hello", argument="world")
# args will be ()
# kwargs will be {"argument": "world"}
assert sample_function(*args, **kwargs) == "world"
```

### Collecting Parameters with Variable Arguments

```python
from requisites import collect_params

def complex_function(a, b, *args, c, d=1, **kwargs):
    return "OK"

# Example 1: Handling required parameters
args, kwargs = collect_params(complex_function, "hello", "world", c="see")
# args will be ("hello", "world")
# kwargs will be {"c": "see", "d": 1}
assert complex_function(*args, **kwargs) == "OK"

# Example 2: Handling extra positional and keyword arguments
args, kwargs = collect_params(complex_function, "hello", "world", "!", c="see", e="extra", f="fun")
# args will be ("hello", "world", "!")
# kwargs will be {"c": "see", "d": 1, "e": "extra", "f": "fun"}
assert complex_function(*args, **kwargs) == "OK"
```
