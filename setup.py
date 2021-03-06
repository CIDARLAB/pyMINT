# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='pymint',
    version='0.1.0',
    description='MINT is a language to describe Microfluidic Hardware Netlists. MINT is the name of the Microfluidic Netlist language used to describe microfluidic devices for Fluigi to place and route. Mint is a flavor of (MHDL) Microfluidic Hardware Description Language that can be used to represent Microfluidic Circuits.',
    python_requires='==3.8.*,>=3.8.0',
    author='Radhakrishna Sanka',
    author_email='rkrishnasanka@gmail.com',
    license='BSD-3-Clause',
    packages=['mint', 'mint.constraints'],
    package_dir={"": "."},
    package_data={"mint": ["antlr/*.interp", "antlr/*.tokens"]},
    install_requires=[
        'antlr4-python3-runtime==4.*,>=4.8.0', 'install==1.*,>=1.3.3',
        'parchmint', 'pip==20.*,>=20.2.2'
    ],
    dependency_links=['/home/krishna/CIDAR/pyparchmint'],
)
