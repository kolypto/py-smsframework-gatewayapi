import sys
from datetime import datetime
from flask import Blueprint
from flask.globals import request, g

from smsframework.data import IncomingMessage
from smsframework_gatewayapi.status import GatewayApiMessageStatus

bp = Blueprint('smsframework-gatewayapi', __name__, url_prefix='/')


@bp.route('/im', methods=('POST',))
def im():
    """ Incoming message handler

    Docs: https://gatewayapi.com/docs/rest.html#mo-sms-receiving-sms-es
    """
    req = request.get_json()

    # Check
    for n in ('id', 'msisdn', 'message', 'senttime'):
        assert n in req, 'Received a message with missing "{}" field: {}'.format(n, req)

    # Message text
    body = req.pop('message')
    if 'encoding' in req:
        pass  # TODO: implement encoding
        # if sys.version_info[0] == 2:
        #     req['text'] = req['text'].decode(req['encoding'])  # Python 2: str -> unicode
        # else:
        #     req['text'] = bytes(req['text'], 'latin-1').decode(req['encoding'])  # Python 3: str -> bytes -> unicode

    # IncomingMessage
    message = IncomingMessage(
        src=str(req.pop('msisdn')),
        body=body,
        msgid=str(req.pop('id')),
        dst=str(req.pop('receiver')),
        rtime=datetime.utcfromtimestamp(req.pop('senttime')),  # TODO: What timezone?
        meta=req
    )

    # Process it
    " :type: smsframework.IProvider.IProvider "
    g.provider._receive_message(message)  # exception results in code 500 ; they will retry

    # Ack
    return '<ack refno="{msgid}" errorcode="0" />'.format(msgid=message.msgid)


@bp.route('/status', methods=('POST',))
def status():
    """ Incoming status report

    Docs: https://gatewayapi.com/docs/rest.html#delivery-status-notification
    """
    req = request.get_json()

    # Check fields
    for n in ('status', 'id', 'time'):
        assert n in req, 'Received a status with missing "{}" field: {}'.format(n, req)

    # MessageStatus
    status = GatewayApiMessageStatus.from_code(
        req.pop('status').title(),  # comes in in all caps
        msgid=str(req.pop('id')),  # (integer)
        rtime=datetime.utcfromtimestamp(req.pop('time')),  # TODO: What timezone?
        meta=req
    )

    # Process it
    g.provider._receive_status(status)  # exception results in code 500 ; they will retry

    # Ack with anything
    return 'okay-okay! :)'
