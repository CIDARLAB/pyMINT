[![Documentation Status](https://readthedocs.org/projects/pymint/badge/?version=latest)](https://pymint.readthedocs.io/en/latest/?badge=latest)


# MINT <img align="right" src="MINTLogo.png" width="250">

MINT is a language to describe Microfluidic Hardware Netlists. MINT is the name of the Microfluidic Netlist language used to describe microfluidic devices for Fluigi to place and route. MINT is a flavor of (MHDL) Microfluidic Hardware Description Language that can be used to represent Microfluidic Circuits.

## Installation

### From pypi


```
pip install pymint
```

### From Source

Clone this repository

```
git clone https://github.com/CIDARLAB/pymint
```

Go to the cloned directory and use poetry to install dependencies

```
poetry install 
```

Installl it into the development environment
```
pip install .
```

### Add as a development dependency


**pip**

```
pip install -e /path/to/pymint/repository
```

**poetry**

Add the following line into the `pyproject.toml` -> `[tool.poetry.dev-dependencies]` section:

```
[tool.poetry.dev-dependencies]

...

parchmint = {path = "/path/to/directory/pymint", develop=true}

```

## Documentation

Documentation for the `pymint` package is available at [readthedocs](https://pymint.readthedocs.io/en/latest/). Since the device model used within `pymint` is a `parchmint` device, we recommend that you also check out the [documentation](https://parchmint.readthedocs.io/en/latest/) for the `parchmint` package.

## Quick Start Example

```

from pymint.mintdevice import MINTDevice

import math
import random

# Open the file
mint_device = MINTDevice.from_mint_file("test.mint")

# List all the components in the file
for component in mint_device.device.components:
    print(component.ID)
    print("x size: ", component.xspan)
    print("y size: ", component.yspan)

# List all the connections in the device    
for connection in mint_device.device.connections:
    print(connection.ID)

```


## ANTLR Parser Generation

ANTLR (ANother Tool for Language Recognition) is a parser generator for reading, processing, executing, or translating structured text or binary files. We defined the MINT language syntax in grammar file `mint.g4` that can be used by ANTLR to generates a parser and utilize the antlr package to automatically build and walk the parse tree.

### Installation

To install and work with ANTLR, one can follow the instructions at the [ANTLR Quick Start](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)



```
antlr4 -o ./pymint/antlrgen -listener -visitor -Dlanguage=Python3 -lib . ./mint.g4
```
