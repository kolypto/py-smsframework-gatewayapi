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
        code = int(rv['code'], 16)  # str hex -> int
        if code in InsufficientFundsError.codes:
            C = InsufficientFundsError
        elif 0x0200 <= code <= 0x0311:
            C = ApiError
        else:
            C = cls
        return C(code, rv['message'])


# https://gatewayapi.com/docs/errors.html

class ConnectionError(GatewayAPIProviderError, exc.ConnectionError):
    """ Can't connect to the API endpoint """


class ApiError(GatewayAPIProviderError, exc.RequestError):
    """ These cover codes 0x0100-0x07FF. You might encounter these when communicating with one of our API’s """


class InsufficientFundsError(GatewayAPIProviderError, exc.CreditError):
    """ Insufficient credit """
    codes = (0x1092, 0x0216)
