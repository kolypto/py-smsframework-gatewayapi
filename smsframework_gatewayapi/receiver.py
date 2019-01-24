import jwt
from datetime import datetime
from flask import Blueprint, Response
from flask.globals import request, g, current_app

from smsframework.data import IncomingMessage
from smsframework_gatewayapi.status import GatewayApiMessageStatus

bp = Blueprint('smsframework-gatewayapi', __name__, url_prefix='/')


@bp.route('/callback', methods=('POST',))
def callback():
    """ Combined Message / Status handler """
    # Security: JWT header
    if g.provider._jwt_secret is not None:
        try:
            jwt.decode(request.headers.get('X-GWAPI-Signature', ''), g.provider._jwt_secret, algorithms=['HS256'])
        except jwt.DecodeError as e:
            return Response('Insecure: JWT header error. Wrong JWT secret token in config?', status=403)
    # Handle
    req = request.get_json()
    if 'message' in req:
        return im(req)
    else:
        return status(req)


def im(req):
    """ Incoming message handler

    Docs: https://gatewayapi.com/docs/rest.html#mo-sms-receiving-sms-es
    """
    # Check
    for n in ('id', 'msisdn', 'message', 'senttime'):
        assert n in req, 'Received a message with missing "{}" field: {}'.format(n, req)

    # Message text
    body = req.pop('message')

    # Encoding
    if 'encoding' in req:
        pass  # TODO: implement encoding

    # IncomingMessage
    message = IncomingMessage(
        src=str(req.pop('msisdn')),
        body=body,
        msgid=str(req.pop('id')),
        dst=str(req.pop('receiver')),
        rtime=datetime.utcfromtimestamp(req.pop('senttime')),  # Time's in UTC
        meta=req
    )

    # Process it
    " :type: smsframework.IProvider.IProvider "
    g.provider._receive_message(message)  # exception results in code 500 ; they will retry

    # Ack
    return 'got it!'


def status(req):
    """ Incoming status report

    Docs: https://gatewayapi.com/docs/rest.html#delivery-status-notification
    """
    # Check fields
    for n in ('status', 'id', 'time'):
        assert n in req, 'Received a status with missing "{}" field: {}'.format(n, req)

    # MessageStatus
    status = GatewayApiMessageStatus.from_code(
        req.pop('status').title(),  # comes in in all caps
        msgid=str(req.pop('id')),  # (integer)
        rtime=datetime.utcfromtimestamp(req.pop('time')),  # Time's in UTC
        meta=req
    )

    # Process it
    g.provider._receive_status(status)  # exception results in code 500 ; they will retry

    # Ack with anything
    return 'okay, thanks!'
