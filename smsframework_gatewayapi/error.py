""" GatewayApi error codes """

from smsframework import exc


class GatewayAPIProviderError(exc.ProviderError):
    """ Any error reported by GatewayApi """

    def __init__(self, code, message=''):
        self.code = code
        super(GatewayAPIProviderError, self).__init__(
            '#0x{:04X}: {}'.format(self.code, message)
        )

    @classmethod
    def from_response_value(cls, rv):
        """ Create an error from response """
        # Get code
        # https://gatewayapi.com/docs/errors.html
        code = int(rv['code'], 16)  # str hex -> int
        # Choose class
        if code in InsufficientFundsError.codes:
            C = InsufficientFundsError
        elif 0x0200 <= code <= 0x0311:
            C = ApiError
        else:
            C = cls
        # Format message
        msg = rv['message']
        if rv['variables']:
            # %1 and %2, never %3
            msg = msg.replace('%1', '{0}').replace('%2', '{1}').format(*rv['variables'])
        # Done
        return C(code, msg)


class ConnectionError(GatewayAPIProviderError, exc.ConnectionError):
    """ Can't connect to the API endpoint """


class ApiError(GatewayAPIProviderError, exc.RequestError):
    """ These cover codes 0x0100-0x07FF. You might encounter these when communicating with one of our APIs """


class InsufficientFundsError(GatewayAPIProviderError, exc.CreditError):
    """ Insufficient credit """
    codes = (0x1092, 0x0216)
