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

* `key`: API key
* `secret`: API secret

Example
=======

```python
from smsframework import Gateway, OutgoingMessage
from smsframework_gatewayapi import GatewayAPIProvider

# Init Gateway, Provider
gateway = Gateway()
gateway.add_provider('gapi', GatewayAPIProvider,
    key='AAABBBBCCCCDDDD', secret='XAD*HHH(aaaaa'
)

# Send a regular message
gateway.send(OutgoingMessage('+19991112233', 'Test'))

# Send a premium message
gateway.send(OutgoingMessage('+19991112233', 'Test').options(escalate=True))
```



Supported Options
=================

* `validity_period`: Message expiration time in minutes
* `senderId`: Alpha-numeric SenderId
* `escalate`: Premium message



Provider-Specific Parameters
============================

See <https://gatewayapi.com/docs/rest.html#post--rest-mtsms>

Limitations
===========

Incoming messages are currently not supported.
