# hcscom

![coverage](https://gitlab.com/Menschel/hcscom/badges/master/coverage.svg)
![pipeline](https://gitlab.com/Menschel/hcscom/badges/master/pipeline.svg)

[Documentation](https://menschel.gitlab.io/hcscom/)

A python3 class for remote control of manson hcs lab power supplies.

Manson lab power supply units can be controlled via usb.

Communication is done via a builtin CP210x usb-serial bridge and 8N1@9600 port settings.


# clones

Some PeakTech branded devices have proven to be Manson devices, i.e.

https://www.peaktech.de/productdetail/kategorie/schaltnetzteile/produkt/p-1575.html

returns `HCS-3402` as response to `GMOD` command which is

https://www.manson.com.hk/product/hcs-3402-usb/

# License
This software is distributed under GPLv3 with some the extension that it's not to be used for commercial purposes.
It is explicitly denied that any company or organization monetizes on this software. Monetize does not only mean money,
it means gaining a competitive advantage of any kind by using this software.
In addition, the author explicitly denies the usage for people associated with military and
government agencies of any kind to whatever degree.

This extension is a reaction to some blunt support request from 

Technica Engineering GmbH  
Leopoldstraße 236  
D - 80807 München

in May 2022 to basically fix problems they had during commercial usage of this software, for free.

# Deprecation of PyPi Packages
Packages on PyPi are no longer updated due to attempts of the Python Software Foundation to enforce new rules and basically flush out 
developers who do not consent.  
Recent packages can be installed directly from git, i.e.   
```pip install git+https://gitlab.com/Menschel/hcscom.git --upgrade```