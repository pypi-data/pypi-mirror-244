import json
import logging
import os
import threading
import uuid

from . import interceptor_setup
from .backend import ShieldRestHttpClient, ShieldAccessRequest
from .exception import PAIGException, AccessControlException
from .message import ErrorMessage, InfoMessage, WarningMessage

_logger = logging.getLogger(__name__)


class PAIGPlugin:
    """
    Base plugin for Privacera AI Governance (PAIG).

    This class provides the foundational functionality for PAIG plugins,
    including method interception and user_name context management.
    """

    USER_CONTEXT = "user_context"
    """This is the key stored in thread-local storage for the user_name context."""

    def __init__(self, **kwargs):
        """
        Initializes an instance of the PAIGPlugin class.

        Args:
            tenant_id (str): The ID of the tenant using the plugin. TODO: Temporarily added for testing purpose.
            api_key (str, optional): The API key. If not provided, it can be obtained from
                                     the 'api_key_provider' or the environment variable
                                     'PRIVACERA_APPLICATION_KEY'.
            api_key_provider (APIKeyProvider, optional): An instance of a class implementing the
                                                                'APIKeyProvider' interface to retrieve
                                                                the application key.
            application_key (str): The application id for the client making requests.
            client_application_key (str): The client application id for the client making requests.
            libs: A list of libraries to intercept methods from.

        Attributes:
            shield_base_url (str): The base URL for the Shield service.
            thread_local: An instance of threading.local() for managing thread-local data.
        """

        if "application_config_file" in kwargs:
            plugin_app_config_dict = self.load_plugin_application_configs_from_file(kwargs["application_config_file"])
        elif "application_config" in kwargs:
            application_config_str = kwargs["application_config"]
            if isinstance(application_config_str, str):
                try:
                    plugin_app_config_dict = json.loads(application_config_str)
                except Exception:
                    _logger.exception(f"Error loading plugin application configs from string {application_config_str}")
                    raise PAIGException(ErrorMessage.INVALID_APPLICATION_CONFIG_FILE)
            elif isinstance(application_config_str, dict):
                plugin_app_config_dict = application_config_str
        else:
            plugin_app_config_dict = self.read_options_from_app_config()

        self.enable_privacera_shield = plugin_app_config_dict.get("enablePrivaceraShield", True)
        self.client_application_key = plugin_app_config_dict.get("clientApplicationKey", "*")
        self.application_id = plugin_app_config_dict.get("applicationId")
        self.application_key = plugin_app_config_dict.get("applicationKey")
        self.tenant_id = plugin_app_config_dict.get("tenantId")
        self.shield_base_url = plugin_app_config_dict.get("apiServerUrl")
        self.api_key = plugin_app_config_dict.get("apiKey")
        self.access_request_connect_timeout = plugin_app_config_dict.get("accessRequestConnectTimeout", 2.0)
        self.access_request_read_timeout = plugin_app_config_dict.get("accessRequestReadTimeout", 7.0)
        self.http_max_retries = plugin_app_config_dict.get("httpMaxRetries", 4)
        self.http_retry_backoff_factor = plugin_app_config_dict.get("httpRetryBackoffFactor", 1)
        self.http_allowed_methods = plugin_app_config_dict.get("httpAllowedMethods", ["GET", "POST", "PUT", "DELETE"])
        self.http_status_retry_forcelist = plugin_app_config_dict.get("httpStatusRetryForceList", [500, 502, 503, 504])

        self.shield_server_key_id = plugin_app_config_dict.get("shieldServerKeyId")
        self.shield_server_public_key = plugin_app_config_dict.get("shieldServerPublicKey")
        self.shield_plugin_key_id = plugin_app_config_dict.get("shieldPluginKeyId")
        self.shield_plugin_private_key = plugin_app_config_dict.get("shieldPluginPrivateKey")

        # Then overriding the configurations from environment variables
        if "PRIVACERA_SHIELD_ENABLE" in os.environ:
            self.enable_privacera_shield = os.getenv("PRIVACERA_SHIELD_ENABLE", "true").lower() == "true"
            _logger.info(
                InfoMessage.PRIVACERA_SHIELD_IS_ENABLED.format(is_enabled=self.enable_privacera_shield))

        if self.shield_base_url is None:
            # TODO: Needs to be fixed to final URL
            self.shield_base_url = "https://main-paig-shield.privacera.me"  # Set the base URL for Shield

            # This is an override to be used during testing
            if "shield_base_url" in kwargs:
                self.shield_base_url = kwargs["shield_base_url"]

        if self.tenant_id is None:
            # TODO: added for testing, needs to be removed
            if "tenant_id" in kwargs:
                self.tenant_id = kwargs["tenant_id"]
            # else:
            #     raise PAIGException(ErrorMessage.TENANT_ID_NOT_PROVIDED)

        if self.api_key is None:
            if "api_key" in kwargs:
                self.api_key = kwargs["api_key"]
            elif "api_key_provider" in kwargs:
                self.api_key = kwargs["api_key_provider"].get_key()
            else:
                self.api_key = os.getenv('PRIVACERA_SHIELD_API_KEY')

        if self.api_key is None:
            raise PAIGException(ErrorMessage.API_KEY_NOT_PROVIDED.format())

        if self.application_key is None:
            # this will be a fallback value, as client should be able to set it in the request context
            self.application_key = None
            if "application_key" in kwargs:
                self.application_key = kwargs["application_key"]

        if self.client_application_key is None:
            # this will be a fallback value, as client should be able to set it in the request context
            self.client_application_key = None
            if "client_application_key" in kwargs:
                self.client_application_key = kwargs["client_application_key"]

        self.frameworks = None
        if "frameworks" in kwargs:
            self.frameworks = kwargs["frameworks"]
        else:
            raise PAIGException(ErrorMessage.FRAMEWORKS_NOT_PROVIDED.format())

        # TODO - do we need this if we have application_key:
        if not self.application_id:
            if _logger.isEnabledFor(logging.DEBUG):
                _logger.debug("Application ID not provided")

        self.shield_server_key_id = plugin_app_config_dict.get("shieldServerKeyId")
        self.shield_server_public_key = plugin_app_config_dict.get("shieldServerPublicKey")
        self.shield_plugin_key_id = plugin_app_config_dict.get("shieldPluginKeyId")
        self.shield_plugin_private_key = plugin_app_config_dict.get("shieldPluginPrivateKey")

        if not self.shield_server_key_id:
            if "shield_server_key_id" in kwargs:
                self.shield_server_key_id = kwargs["shield_server_key_id"]
            else:
                raise PAIGException(ErrorMessage.SHIELD_SERVER_KEY_ID_NOT_PROVIDED.format())

        if not self.shield_server_public_key:
            if "shield_server_public_key" in kwargs:
                self.shield_server_public_key = kwargs["shield_server_public_key"]
            else:
                raise PAIGException(ErrorMessage.SHIELD_SERVER_PUBLIC_KEY_NOT_PROVIDED.format())

        if not self.shield_plugin_key_id:
            if "shield_plugin_key_id" in kwargs:
                self.shield_plugin_key_id = kwargs["shield_plugin_key_id"]
            else:
                raise PAIGException(ErrorMessage.SHIELD_PLUGIN_KEY_ID_NOT_PROVIDED.format())

        if not self.shield_plugin_private_key:
            if "shield_plugin_private_key" in kwargs:
                self.shield_plugin_private_key = kwargs["shield_plugin_private_key"]
            else:
                raise PAIGException(ErrorMessage.SHIELD_PLUGIN_PRIVATE_KEY_NOT_PROVIDED.format())

        encryption_keys_info = {
            "shield_server_key_id": self.shield_server_key_id,
            "shield_server_public_key": self.shield_server_public_key,
            "shield_plugin_key_id": self.shield_plugin_key_id,
            "shield_plugin_private_key": self.shield_plugin_private_key
        }

        http_retry_configs = {
            "max_retries": self.http_max_retries,
            "backoff_factor": self.http_retry_backoff_factor,
            "allowed_methods": self.http_allowed_methods,
            "status_forcelist": self.http_status_retry_forcelist
        }

        self.thread_local = threading.local()
        self.thread_local_rlock = threading.RLock()
        self.shield_client = ShieldRestHttpClient(base_url=self.shield_base_url, tenant_id=self.tenant_id,
                                                  api_key=self.api_key, encryption_keys_info=encryption_keys_info,
                                                  access_request_connect_timeout=self.access_request_connect_timeout,
                                                  access_request_read_timeout=self.access_request_read_timeout,
                                                  http_retry_configs=http_retry_configs)

        self.shield_client.init_shield_server()

        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"PAIGPlugin initialized with {self.__dict__}")

    def find_config_file(self, directory):
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.startswith("privacera-shield-") and filename.endswith("-config.json"):
                    return os.path.join(directory, filename)
        return None  # No matching file found

    def read_options_from_app_config(self):
        # Get the application config file path from the environment variable
        application_config_file = os.getenv("PRIVACERA_SHIELD_CONF_FILE")

        application_config_dir = None
        if application_config_file is None:
            application_config_dir = os.path.join(os.getcwd(), os.getenv("PRIVACERA_SHIELD_CONF_DIR", "privacera"))
            application_config_file = self.find_config_file(application_config_dir)

        if application_config_file is None or not os.path.exists(application_config_file):
            if application_config_dir:
                # Log the directory if application_config_file is still None
                _logger.warning(
                    WarningMessage.ERROR_MESSAGE_CONFIG_FILE_NOT_FOUND.format(file_path=application_config_dir)
                )
            else:
                # Log a warning if the config file is not found or doesn't exist
                _logger.warning(
                    WarningMessage.ERROR_MESSAGE_CONFIG_FILE_NOT_FOUND.format(file_path=application_config_file)
                )
            raise PAIGException(ErrorMessage.API_KEY_NOT_PROVIDED.format())

        # Load and return the plugin application configs from the config file
        return self.load_plugin_application_configs_from_file(application_config_file)

    def load_plugin_application_configs_from_file(self, app_config_file_path: str):
        try:
            with open(app_config_file_path, 'r') as config_file:
                plugin_app_config_dict = json.load(config_file)
                return plugin_app_config_dict
        except Exception:
            _logger.exception(f"Error loading plugin application configs from file {app_config_file_path}")
            raise PAIGException(
                WarningMessage.ERROR_MESSAGE_CONFIG_FILE_NOT_FOUND.format(file_path=app_config_file_path)
                )

    def get_frameworks_to_intercept(self):
        return self.frameworks

    def get_shield_client(self):
        return self.shield_client

    def get_application_key(self):
        return self.get_current("application_key", self.application_key)

    def get_client_application_key(self):
        return self.get_current("client_application_key", self.client_application_key)

    def setup(self):
        """
        Set up the PAIG plugin by intercepting methods for enhanced functionality.
        """
        if self.enable_privacera_shield:
            interceptor_setup.setup(self)

    def set_current_user(self, username):
        """
        Set the current user_name context for the PAIG plugin.

        Args:
            username (str): The username of the current user_name.

        Notes:
            This method needs to be called before making any request to LLM
        """
        self.set_current(username=username)

    def get_current_user(self):
        """
        Get the current user_name from the PAIG plugin's context.

        Returns:
            str: The username of the current user_name.

        Raises:
            Exception: If the current user_name is not set in the context.
        """
        return self.get_current("username")

    def generate_request_id(self):
        """
        Generate a unique Request ID.

        Returns:
            str: A unique Request ID in UUID format.
        """
        return str(uuid.uuid1())

    def generate_conversation_thread_id(self):
        """
        Generate a unique Thread ID for the conversation.

        Returns:
            str: A unique Thread ID in UUID format.
        """
        return str(uuid.uuid1())

    def set_current(self, **kwargs):
        """
        Set any name-value into current thread-local context for the PAIG plugin.
        :param kwargs: name=value pairs to be set in the context
        :return: nothing
        """
        with self.thread_local_rlock:
            user_context = getattr(self.thread_local, PAIGPlugin.USER_CONTEXT, {})
            user_context.update(kwargs)
            setattr(self.thread_local, PAIGPlugin.USER_CONTEXT, user_context)

    def get_current(self, key, default_value=None):
        """
        Get the value of the given key from the current thread-local context for the PAIG plugin.
        :param key:
        :param default_value: returned if the key does not exist
        :return:
        """
        with self.thread_local_rlock:
            user_context = getattr(self.thread_local, PAIGPlugin.USER_CONTEXT, {})
            if key in user_context:
                return user_context[key]
            else:
                return default_value

    def clear(self):
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug(f"Clearing thread-local context for PAIG plugin")
        with self.thread_local_rlock:
            delattr(self.thread_local, PAIGPlugin.USER_CONTEXT)


class PAIGPluginContext:
    """
    This class provides a context manager for the PAIG plugin.
    """

    def __init__(self, **kwargs):
        """
        Initializes an instance of the PAIGPluginContext class.

        Args:
            kwargs: The name-value pairs to be set in the context.

        Attributes:
            kwargs: The name-value pairs to be set in the context.
        """
        self.kwargs = kwargs

    def __enter__(self):
        """
        Set the name-value pairs in the context.

        Returns:
            PAIGPluginContext: The current instance of the PAIGPluginContext class.
        """
        _paig_plugin.set_current(**self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clear the context.

        Args:
            exc_type: The type of the exception.
            exc_val: The exception value.
            exc_tb: The exception traceback.
        """
        _paig_plugin.clear()


# Global variable to store the PAIGPlugin instance
_paig_plugin: PAIGPlugin = None


def setup(**options):
    """
    This function initializes the PAIGPlugin instance and calls its 'init' method to set up the PAIG plugin.

    Note:
        The global '_paig_plugin' variable is used to store the PAIGPlugin instance for later use.

    """
    global _paig_plugin
    if _paig_plugin is not None:
        #raise PAIGException(ErrorMessage.PAIG_IS_ALREADY_INITIALIZED.format())
        _logger.error(ErrorMessage.PAIG_IS_ALREADY_INITIALIZED.format())
    else:
        _paig_plugin = PAIGPlugin(**options)  # Create an instance of PAIGPlugin
        _paig_plugin.setup()  # Initialize the PAIG plugin
        if _logger.isEnabledFor(logging.INFO):
            _logger.info(InfoMessage.PAIG_IS_INITIALIZED.format())


def set_current_user(username):
    """
    Set the current user_name context for the PAIG plugin.

    Args:
        username (str): The username of the current user_name.

    Note:
        This function sets the user_name context using the 'set_current_user_context' method of the PAIGPlugin instance
        stored in the global '_paig_plugin' variable.

    """
    global _paig_plugin
    _paig_plugin.set_current_user(username)  # Set the current user_name


def get_current_user():
    _paig_plugin.get_current("username")


def set_current(**kwargs):
    global _paig_plugin
    _paig_plugin.set_current(**kwargs)


def get_current(key, default_value=None):
    ret_val = _paig_plugin.get_current(key, default_value)
    return ret_val


def clear():
    global _paig_plugin
    _paig_plugin.clear()


def create_shield_context(**kwargs):
    return PAIGPluginContext(**kwargs)


def check_access(**kwargs):
    if "text" not in kwargs:
        raise PAIGException(ErrorMessage.PROMPT_NOT_PROVIDED.format())
    if "conversation_type" not in kwargs:
        raise PAIGException(ErrorMessage.CONVERSATION_TYPE_NOT_PROVIDED.format())
    text = kwargs["text"]
    conversation_type = kwargs["conversation_type"]
    access_request = ShieldAccessRequest(
        application_key=_paig_plugin.get_application_key(),
        client_application_key=_paig_plugin.get_client_application_key(),
        conversation_thread_id=_paig_plugin.generate_conversation_thread_id(),
        request_id=_paig_plugin.generate_request_id(),
        user_name=_paig_plugin.get_current_user(),
        request_text=[text],
        conversation_type=conversation_type
    )
    access_result = _paig_plugin.get_shield_client().is_access_allowed(request=access_request)
    if not access_result.get_is_allowed():
        raise AccessControlException(access_result.get_response_messages()[0].get_response_text())
    else:
        return access_result.get_response_messages()[0].get_response_text()


def dummy_access_denied():
    raise AccessControlException("Access Denied")
