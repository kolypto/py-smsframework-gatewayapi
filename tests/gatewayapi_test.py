# -*- coding: utf-8 -*-

import unittest

from flask import Flask
from requests_mock import Mocker

from smsframework import Gateway, OutgoingMessage
from smsframework_gatewayapi import GatewayAPIProvider, error


import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class GatewayAPIProviderTest(unittest.TestCase):
    def setUp(self):
        # Gateway
        gw = self.gw = Gateway()
        gw.add_provider('main', GatewayAPIProvider,
                        key='a', secret='b')

        # Flask
        app = self.app = Flask(__name__)

        # Register receivers
        gw.receiver_blueprints_register(app, prefix='/in-sms/')

    def _test_send_request(self, om, request_json, status_code, response_json):
        with Mocker() as m:
            m.post('https://gatewayapi.com/rest/mtsms',
                   status_code=status_code,
                   headers={},
                   additional_matcher=lambda req: request_json is None or req.json() == request_json,
                   json=response_json)

            return self.gw.send(om)

    def test_send(self):
        """ Send an SMS """
        # Test 1: simple message
        om = self._test_send_request(OutgoingMessage('+1999', 'Test'),
                                     {"message": "Test", "recipients": [{"msisdn": "1999"}]},
                                     200, {'ids': [123]})

        self.assertEqual(om.msgid, '123')

        # Test 2: options
        om = self._test_send_request(OutgoingMessage('+1999', 'Test').options(escalate=True, senderId='kolypto', expires=100),
                                     {"message": "Test", "recipients": [{"msisdn": "1999"}],
                                      'class': 'premium', 'sender': 'kolypto', 'validity_period': 6000},
                                     200, {'ids': [123]})

        self.assertEqual(om.msgid, '123')

        # Test 3: errors (from the docs)
        self.assertRaises(error.ApiError, self._test_send_request,
                          OutgoingMessage('+1999', 'Test'), None,
                          403, {"code": "0x0213", "incident_uuid": "d8127429-fa0c-4316-b1f2-e610c3958f43",
                                "message": "Unauthorized IP-address: %1", "variables": ["1.2.3.4"]}
                          )
        self.assertRaises(error.InsufficientFundsError, self._test_send_request,
                          OutgoingMessage('+1999', 'Test'), None,
                          403, {"code": "0x0216", "incident_uuid": "d8127429-fa0c-4316-b1f2-e610c3958f43",
                                "message": "Insufficient credit", "variables": []}
                          )