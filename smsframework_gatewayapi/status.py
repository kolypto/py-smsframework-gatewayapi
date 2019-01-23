from smsframework.data import MessageStatus, MessageAccepted, MessageDelivered, MessageExpired, MessageError

class GatewayApiMessageStatus(MessageStatus):
    """ Base Message Status for GatewayApi """

    @classmethod
    def from_code(cls, status, **kwargs):
        """ Instantiate one of subclasses by code

            :rtype: type
        """
        for C in cls.__subclasses__():
            if C.status == status:
                return C(**kwargs)
        return cls(**kwargs)


class Scheduled(GatewayApiMessageStatus, MessageAccepted):
    """ Used for messages where you set a sendtime in the future. """
    status_code = 10
    status = 'Scheduled'

class Buffered(GatewayApiMessageStatus, MessageAccepted):
    """ The message is held in our internal queue and awaits delivery to the mobile network. """
    status_code = 11
    status = 'Buffered'

class Enroute(GatewayApiMessageStatus, MessageAccepted):
    """ Message has been sent to mobile network, and is on its way to its final destination. """
    status_code = 12
    status = 'Enroute'

class Delivered(GatewayApiMessageStatus, MessageDelivered):
    """ The end user's mobile device has confirmed the delivery, and if message is charged the charge was successful. """
    status_code = 20
    status = 'Delivered'

class Accepted(GatewayApiMessageStatus, MessageDelivered):
    """ The mobile network has accepted the message on the end users behalf. """
    status_code = 21
    status = 'Accepted'

class Expired(GatewayApiMessageStatus, MessageExpired):
    """ Message has exceeded its validity period without getting a delivery confirmation. No further delivery attempts. """
    status_code = 41
    status = 'Expired'

class Deleted(GatewayApiMessageStatus, MessageError):
    """ Message was canceled. """
    status_code = 42
    status = 'Deleted'

class Undeliverable(GatewayApiMessageStatus, MessageError):
    """ Message is permanently undeliverable. Most likely an invalid MSISDN. """
    status_code = 43
    status = 'Undeliverable'

class Rejected(GatewayApiMessageStatus, MessageError):
    """ The mobile network has rejected the message. If this message was charged, the charge has failed. """
    status_code = 44
    status = 'Rejected'

class Skipped(GatewayApiMessageStatus, MessageError):
    """ The message was accepted, but was deliberately ignored due to network-specific rules. """
    status_code = 45
    status = 'Skipped'
