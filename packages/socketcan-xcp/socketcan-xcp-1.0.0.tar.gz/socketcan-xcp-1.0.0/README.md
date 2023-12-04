# socketcan-xcp

![coverage](https://gitlab.com/Menschel/socketcan-xcp/badges/master/coverage.svg)
![pipeline](https://gitlab.com/Menschel/socketcan-xcp/badges/master/pipeline.svg)

[Documentation](https://menschel.gitlab.io/socketcan-xcp/)

A python 3 interface to Universal Measurement and Calibration Protocol XCP

# Description

Goal of this project is to make XCP available in python in a "pythonic" way.

Keep implementation as simple as possible.
Use python3 built-in functions and bytearrays as well as standard modules like struct and enum wherever possible.

# Why yet another implementation of XCP

While there is pyxcp implementation available, it has Windows dependencies and is in general not feasible to adapt.
Instead, this XCP implementation is done from scratch in pure python.

# License
This software is distributed under GPLv3 with some extension because GPLv3 did not manage to deny
criminal misuse by organizations.
This software is intended for usage by community and private individuals who are interested in car hacking.
It is explicitly denied that any company or organization monetizes on this software. Monetize does not only mean money,
it means gaining a competitive advantage of any kind by using this software.
The author explicitly denies the usage for people associated with military,
government agencies of any kind to whatever degree, same for car manufacturers and associates.

# Deprecation of PyPi Packages
Packages on PyPi are no longer updated due to attempts of the Python Software Foundation to enforce new rules and basically flush out 
developers who do not consent.  
Recent packages can be installed directly from git, i.e.   
```pip install git+https://gitlab.com/Menschel/socketcan-xcp.git --upgrade```
