[![Build Status](https://api.travis-ci.org/kolypto/py-smsframework-gatewayapi.png?branch=master)](https://travis-ci.org/kolypto/py-smsframework-gatewayapi)
[![Pythons](https://img.shields.io/badge/python-2.7%20%7C%203.4%E2%80%933.7%20%7C%20pypy-blue.svg)](.travis.yml)

SMSframework GatewayAPI Provider
================================

[GatewayAPI](https://gatewayapi.com/app/) Provider for [smsframework](https://pypi.python.org/pypi/smsframework/).



Installation
============

Install from pypi:

    $ pip install smsframework_gatewayapi

To receive SMS messages, you need to ensure that
[Flask microframework](http://flask.pocoo.org) is also installed:


    $ pip install smsframework_gatewayapi[receiver]






Initialization
==============

```python
from smsframework import Gateway
from smsframework_gatewayapi import GatewayAPIProvider

gateway = Gateway()
gateway.add_provider('gapi', GatewayAPIProvider,
    ....
)
```

Config
------

Source: /smsframework_gatewayapi/provider.py

* ``: ...

Example
=======



Supported Options
=================

* ``: ...



Provider-Specific Parameters
============================

* ``: ...


Example:



Limitations
===========

Incoming messages are currently not supported.
