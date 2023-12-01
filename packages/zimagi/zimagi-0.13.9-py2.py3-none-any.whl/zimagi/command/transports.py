from .. import settings, exceptions, utility, transports
from . import response, messages

import re
import logging
import yaml


logger = logging.getLogger(__name__)


class CommandHTTPSTransport(transports.BaseTransport):

    def __init__(self,
        message_callback = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._message_callback = message_callback


    def handle_request(self, method, url, path, headers, params, decoders):
        if re.match(r'^/status/?$', path):
            return self.request_page(url, headers, None, decoders,
                encrypted = False,
                use_auth = False,
                disable_callbacks = True
            )
        if not path or path == '/':
            return self.request_page(url, headers, None, decoders,
                encrypted = False,
                use_auth = True,
                disable_callbacks = True
            )
        return self.request_command(url, headers, params, decoders)


    def request_command(self, url, headers, params, decoders):
        command_response = response.CommandResponse()
        request, request_response = self._request('POST', url,
            stream = True,
            headers = headers,
            params = params,
            encrypted = True,
            use_auth = True
        )
        logger.debug("Stream {} request headers: {}".format(url, headers))

        if request_response.status_code >= 400:
            error = utility.format_response_error(request_response, self.client.cipher)
            raise exceptions.ResponseError(
                error['message'],
                request_response.status_code,
                error['data']
            )
        try:
            for line in request_response.iter_lines():
                message = messages.Message.get(
                    self.decode_message(request, request_response, decoders, message = line, decrypt = False),
                    cipher = self.client.cipher
                )
                if self._message_callback and callable(self._message_callback):
                    self._message_callback(message)

                command_response.add(message)

        except Exception as error:
            logger.debug("Stream {} error response headers: {}".format(url, request_response.headers))
            logger.debug("Stream {} error response params:\n\n{}".format(url, yaml.dump(params)))
            logger.debug("Stream {} error status code: {}".format(url, request_response.status_code))
            raise error

        if settings.COMMAND_RAISE_ERROR and command_response.error:
            raise exceptions.ResponseError(
                command_response.error_message(),
                request_response.status_code
            )
        return command_response
