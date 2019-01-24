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
[Flask microframework](http://flask.pocoo.org) is also installed, as well as the JWT library:


    $ pip install smsframework_gatewayapi[receiver]






Initialization
==============

```python
from smsframework import Gateway
from smsframework_gatewayapi import GatewayAPIProvider

gateway = Gateway()
gateway.add_provider('gapi', GatewayAPIProvider,
    key='AAABBBBCCCCDDDD', secret='XAD*HHH(aaaaa'
)
```

Config
------

Source: /smsframework_gatewayapi/provider.py

* `key`: API key
* `secret`: API secret
* `jwt_secret`: Secret token for the JWT header (only for REST webhook that receives messages)

Example
=======

```python
from smsframework import Gateway, OutgoingMessage

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



Receivers
=========

Source: /smsframework_gatewayapi/receiver.py

GatewayApi uses a single webhook URL to receive both messages and status reports.

Webhook URL: `<provider-name>/callback`

In order to configure it, go to the [API/Webhooks](https://gatewayapi.com/app/settings/web-hooks/) section in the 
control panel, and add a new "REST" webhook.
The URL will be something like this: `http://.../<prefix>/<provider-name>/callback`

In the *Authentication* section, you can specify a JWT secret token. Pass it to the `GatewayAPIProvider` 
in order to have secure message reception.
