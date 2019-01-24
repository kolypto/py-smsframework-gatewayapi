from smsframework import IProvider, OutgoingMessage
from requests_oauthlib import OAuth1Session
from requests import ConnectionError

from . import error


class GatewayAPIProvider(IProvider):
    """ GatewayApi Provider """

    def __init__(self, gateway, name, key, secret, jwt_secret=None):
        """ Configure GatewayApi provider

            :param key: API key
            :param secret: API secret
            :param jwt_secret: JWT secret token
        """
        self._key = key
        self._secret = secret
        self._jwt_secret = jwt_secret
        super(GatewayAPIProvider, self).__init__(gateway, name)

    def send(self, message):
        """ Send a message

            :type message: OutgoingMessage
            :rtype: OutgoingMessage
            """
        # Parameters
        params = {
            'message': message.body,
            'recipients': [{'msisdn': int(message.dst)}],
        }

        #if message.src:
        #if message.provider_options.allow_reply:
        #if message.provider_options.status_report:
        if message.provider_options.expires:
            params['validity_period'] = message.provider_options.expires*60
        if message.provider_options.senderId:
            params['sender'] = message.provider_options.senderId
        if message.provider_options.escalate:
            params['class'] = 'premium'

        params.update(message.provider_params)

        # Send
        try:
            gwapi = OAuth1Session(self._key, client_secret=self._secret)
            res = gwapi.post('https://gatewayapi.com/rest/mtsms', json=params)
        except ConnectionError as e:
            raise error.ConnectionError(0, str(e))

        # Response
        if res.status_code != 200:
            raise error.GatewayAPIProviderError.from_response_value(res.json())
        else:
            rv = res.json()
            message.msgid = str(rv['ids'][0])
            return message


    def make_receiver_blueprint(self):
        """ Create the receiver blueprint """
        from . import receiver
        return receiver.bp

    #region Public

    #endregion
