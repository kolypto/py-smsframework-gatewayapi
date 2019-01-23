# -*- coding: utf-8 -*-

import unittest

from flask import Flask
from requests_mock import Mocker

from smsframework import Gateway, OutgoingMessage, IncomingMessage
from smsframework_gatewayapi import GatewayAPIProvider, error, status


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
        gw.add_provider('gapi', GatewayAPIProvider,
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

        # Test 3: error (from the docs)
        self.assertRaises(error.ApiError, self._test_send_request,
                          OutgoingMessage('+1999', 'Test'), None,
                          403, {"code": "0x0213", "incident_uuid": "d8127429-fa0c-4316-b1f2-e610c3958f43",
                                "message": "Unauthorized IP-address: %1", "variables": ["1.2.3.4"]}
                          )
        # Test 4: Insufficient funds
        self.assertRaises(error.InsufficientFundsError, self._test_send_request,
                          OutgoingMessage('+1999', 'Test'), None,
                          403, {"code": "0x0216", "incident_uuid": "d8127429-fa0c-4316-b1f2-e610c3958f43",
                                "message": "Insufficient credit", "variables": []}
                          )

    def test_receive_message(self):
        """ Test message receipt """

        # Message receiver
        messages = []
        self.gw.onReceive += lambda message: messages.append(message)

        with self.app.test_client() as c:
            # Message 1: from the docs
            res = c.post('/in-sms/gapi/im', json={
                "id": 1000001,
                "msisdn": 4587654321,
                "receiver": 451204,
                "message": "foo Hello World",
                "senttime": 1450000000,
                "webhook_label": "test"
            })
            self.assertEqual(res.status_code, 200)
            im = messages.pop()  # type: IncomingMessage
            self.assertEqual(im.provider, 'gapi')
            self.assertEqual(im.msgid, '1000001')
            self.assertEqual(im.src, '4587654321')
            self.assertEqual(im.dst, '451204')
            self.assertEqual(im.body, u'foo Hello World')
            self.assertEqual(im.rtime.isoformat(' '), '2015-12-13 09:46:40')
            self.assertEqual(im.meta, {'webhook_label': 'test'})

            # Message 2: real, unicode

    def test_receive_status(self):
        """ Test status receipt """

        # Status receiver
        statuses = []
        self.gw.onStatus += lambda status: statuses.append(status)

        with self.app.test_client() as c:
            # Status 1: from the docs
            res = c.post('/in-sms/gapi/status', json={
                "id": 1000001,
                "msisdn": 4587654321,
                "time": 1450000000,
                "status": "DELIVERED",
                "userref": "foobar",
                "charge_status": "CAPTURED"
            })
            self.assertEqual(res.status_code, 200)
            st = statuses.pop()
            self.assertIsInstance(st, status.MessageDelivered)
            self.assertIsInstance(st, status.GatewayApiMessageStatus)
            self.assertEqual(st.provider, 'gapi')
            self.assertEqual(st.status_code, 20)
            self.assertEqual(st.status, 'Delivered')
            self.assertEqual(st.accepted, True)
            self.assertEqual(st.delivered, True)
            self.assertEqual(st.expired, False)
            self.assertEqual(st.error, False)
            self.assertEqual(st.msgid, '1000001')
            self.assertEqual(st.rtime.isoformat(' '), '2015-12-13 09:46:40')
            self.assertEqual(st.meta, {'msisdn': 4587654321, 'userref': 'foobar', 'charge_status': 'CAPTURED'})
