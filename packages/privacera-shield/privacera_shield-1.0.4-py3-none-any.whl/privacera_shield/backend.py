import json
import logging
import time

import urllib3
from urllib3 import Timeout, Retry

from . import util
from .PluginAccessRequestEncryptor import PluginAccessRequestEncryptor
from .exception import PAIGException
from .message import ErrorMessage
from .model import ConversationType
from .util import AtomicCounter

_logger = logging.getLogger(__name__)

sequence_number = AtomicCounter()


class ShieldAccessRequest:
    def __init__(self, **kwargs):
        """
        Initialize a ShieldAccessRequest instance.

        Args:
            application_key (str): The Key of the application.
            client_application_key (str): The Key of the client application.
            conversation_thread_id (str): The ID of the conversation thread.
            request_id (str): The Request ID.
            user_name (str): The name of the user making the request.
            request_text (list[str]): The text of the request.
            conversation_type (str): The type of conversation (prompt or reply).

        Note:
            - The conversation_type should be one of the values defined in the ConversationType enum.

        """
        self.application_key = kwargs.get('application_key')
        self.client_application_key = kwargs.get('client_application_key')
        self.conversation_thread_id = kwargs.get('conversation_thread_id')
        self.request_id = kwargs.get('request_id')
        self.user_name = kwargs.get('user_name')
        self.request_text = kwargs.get('request_text')
        self.conversation_type = kwargs.get('conversation_type', ConversationType.PROMPT)
        self.shield_server_key_id = kwargs.get('shield_server_key_id', None)
        self.shield_plugin_key_id = kwargs.get('shield_plugin_key_id', None)

    def to_payload_dict(self):
        """
        Serialize the ShieldAccessRequest instance to a JSON string.

        Returns:
            str: JSON representation of the instance.
        """
        request_dict = {
            # "conversationId": "1001", # Not able to get

            "threadId": self.conversation_thread_id,
            "requestId": self.request_id,

            "sequenceNumber": sequence_number.increment(),
            "requestType": self.conversation_type.lower(),

            "requestDateTime": int(time.time()) * 1000,
            # datetime.now(timezone.utc),
            # utils.get_time_now_utc_str(), # TODO: this is a breaking change from int to iso8601 time format

            "clientApplicationKey": self.client_application_key,
            "applicationKey": self.application_key,

            "userId": self.user_name,

            "context": {},  # Additional context information
            "messages": self.request_text,

            "clientIp": util.get_my_ip_address(),
            "clientHostName": util.get_my_hostname(),

            "shieldServerKeyId": self.shield_server_key_id,
            "shieldPluginKeyId": self.shield_plugin_key_id
        }

        return request_dict


class ResponseMessage:
    def __init__(self, response_message):
        """
        Initialize a ResponseMessage instance.

        Args:
            response_message (dict): A dictionary containing response message data.

        Attributes:
            is_allowed (bool): Indicates whether the access is allowed.
            response_text (str): The response text associated with the message.
        """
        self.response_text = response_message["responseText"]

    def get_response_text(self):
        """
        Get the 'response_text' attribute value.

        Returns:
            str: The response text.
        """
        return self.response_text


class ShieldAccessResult:
    def __init__(self, **kwargs):
        """
        Initialize a ShieldAccessResult instance.

        Args:
            threadId (str): The ID of the thread.
            requestId (str): The ID of the request.
            sequenceNumber (int): The sequence number.
            isAllowed (bool): Indicates whether the access is allowed.
            responseMessages (list): A list of response messages.

        Attributes:
            threadId (str): The ID of the thread.
            requestId (str): The ID of the request.
            sequenceNumber (int): The sequence number.
            isAllowed (bool): Indicates whether the access is allowed.
            responseMessages (list): A list of response messages.
        """
        self.threadId = kwargs.get('threadId')
        self.requestId = kwargs.get('requestId')
        self.sequenceNumber = kwargs.get('sequenceNumber')
        self.isAllowed = kwargs.get('isAllowed')
        self.responseMessages = kwargs.get('responseMessages')

    @classmethod
    def from_json(cls, **response_dict):
        """
        Deserialize a JSON string to create a ShieldAccessResult instance.

        Args:
            response_dict (str): JSON representation of the ShieldAccessResult.

        Returns:
            ShieldAccessResult: An instance of ShieldAccessResult.
        """
        return cls(**response_dict)

    def get_response_messages(self):
        """
        Get a list of ResponseMessage instances from 'responseMessages'.

        Returns:
            list: A list of ResponseMessage instances.
        """
        response_messages = []
        for message in self.responseMessages:
            response_messages.append(ResponseMessage(message))
        return response_messages

    def get_last_response_message(self) -> ResponseMessage:
        """
        Get the last ResponseMessage in the 'responseMessages' list.

        Returns:
            ResponseMessage: The last ResponseMessage.

        Raises:
            Exception: If no responseMessages are found.
        """
        if len(self.responseMessages) == 0:
            raise Exception("No responseMessages found.")

        last_response_message = self.responseMessages[-1]
        return ResponseMessage(last_response_message)

    def get_is_allowed(self):
        """
        Get the 'isAllowed' attribute value.

        Returns:
            bool: True if access is allowed, False otherwise.
        """
        return self.isAllowed

    # def to_dict(self):
    #     return {"threadId": self.threadId,
    #             "requestId": self.requestId,
    #             "sequenceNumber": self.sequenceNumber,
    #             "isAllowed": self.isAllowed,
    #             "responseMessages": [responseMessage.get_response_text() for responseMessage in self.responseMessages]}


class ShieldRestHttpClient:
    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.tenant_id = kwargs['tenant_id'] if 'tenant_id' in kwargs else None
        self.base_url = kwargs['base_url']
        self.api_key = kwargs['api_key']

        self.access_request_connect_timeout = kwargs.get('access_request_connect_timeout', 2.0)
        self.access_request_read_timeout = kwargs.get('access_request_read_timeout', 7.0)

        http_retry_configs = kwargs.get('http_retry_configs', {})

        retries = Retry(total=http_retry_configs.get('max_retries'),
                        backoff_factor=http_retry_configs.get('backoff_factor'),
                        status_forcelist=http_retry_configs.get('status_forcelist'),
                        allowed_methods=http_retry_configs.get('allowed_methods'))
        self.http = urllib3.PoolManager(num_pools=50, maxsize=50, block=True, retries=retries)
        # TODO: add proxy support
        # TODO: add ignore SSL support
        # TODO: expose any metrics

        self.plugin_access_request_encryptor = PluginAccessRequestEncryptor(self.tenant_id,
                                                                            kwargs["encryption_keys_info"])

    def get_default_headers(self):
        headers = dict()
        if self.tenant_id:
            headers["x-tenant-id"] = self.tenant_id
        if self.api_key:
            headers["x-paig-api-key"] = self.api_key
        return headers

    def is_access_allowed(self, request: ShieldAccessRequest) -> ShieldAccessResult:
        """
        Check if access is allowed and return the result.

        Args:
            request (ShieldAccessRequest): The access request to be checked.

        Returns:
            ShieldAccessResult: The result of the access check.
        """

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Access request parameters: {request.to_payload_dict()}")

        # Encrypt the request messages and set the encryption key id and plugin public key in request
        self.plugin_access_request_encryptor.encrypt_request(request)
        request.shield_server_key_id = self.plugin_access_request_encryptor.shield_server_key_id
        request.shield_plugin_key_id = self.plugin_access_request_encryptor.shield_plugin_key_id

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Access request parameters (encrypted): {request.to_payload_dict()}")

        response = self.http.request(method="POST",
                                     url=self.base_url + "/shield/authorize",
                                     headers=self.get_default_headers(),
                                     json=request.to_payload_dict(),
                                     timeout=Timeout(connect=self.access_request_connect_timeout,
                                                     read=self.access_request_read_timeout))

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Access response status (encrypted): {response.status}, body: {response.data}")

        if response.status == 200:
            access_result = ShieldAccessResult.from_json(**response.json())
            if access_result.isAllowed:
                # Decrypt the response messages
                self.plugin_access_request_encryptor.decrypt_response(access_result)
                if _logger.isEnabledFor(logging.DEBUG):
                    _logger.debug(
                        f"Access response status: {response.status}, access_result: {json.dumps(access_result.__dict__)}")
            return access_result
        else:
            error_message = f"Request failed with status code {response.status}: {response.data}"
            _logger.error(error_message)
            raise Exception(error_message)

    def init_shield_server(self) -> None:
        """
        Initialize shield server for the tenant id.
        """
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Initializing shield server for tenant: tenant_id={self.tenant_id}")

        request = {"shieldServerKeyId": self.plugin_access_request_encryptor.shield_server_key_id,
                   "shieldPluginKeyId": self.plugin_access_request_encryptor.shield_plugin_key_id}

        response = self.http.request(method="POST",
                                     url=self.base_url + "/shield/init",
                                     headers=self.get_default_headers(),
                                     json=json.dumps(request),
                                     timeout=Timeout(connect=self.access_request_connect_timeout,
                                                     read=self.access_request_read_timeout))

        if response.status == 200:
            _logger.info(f"Shield server initialized for tenant: tenant_id={self.tenant_id}")
        else:
            error_message = f"Shield server initialization request failed with status code {response.status}: {response.data}"
            _logger.error(error_message)
            raise PAIGException(ErrorMessage.SHIELD_SERVER_INITIALIZATION_FAILED.format())
