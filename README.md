![Docs Status](https://readthedocs.org/projects/pymint/badge/)

# MINT

MINT is a language to describe Microfluidic Hardware Netlists. MINT is the name of the Microfluidic Netlist language used to describe microfluidic devices for Fluigi to place and route. MINT is a flavor of (MHDL) Microfluidic Hardware Description Language that can be used to represent Microfluidic Circuits.



## Documentation

Chechttps://pymint.readthedocs.io/en/latest/


## Updating the ANTLR parser 

```
antlr4 -o ./pymint/antlrgen -listener -visitor -Dlanguage=Python3 -lib . ./mint.g4
```