from enum import Enum, auto
import logging


class BaseMessage(Enum):
    def format(self, level, **kwargs):
        """
        It appends PAIG-5x as logging.ERROR is 50
        :param kwargs:
        :return: formatted string with PAIG-5x prefix
        """
        return f'{logging.getLevelName(level)}: PAIG-{str(self.value[0])}: {self.value[1].format(**kwargs)}'


class ErrorMessage(BaseMessage):
    """
    Enum that has all the error messages. Do not change the order of the messages. Add new message to the end of the
    list always so that the order is not changed.
    """
    TENANT_ID_NOT_PROVIDED = 400001, "Tenant ID is not provided"
    API_KEY_NOT_PROVIDED = 400002, "Application config file not found. Cannot initialize Shield Plugin Library."
    PAIG_IS_ALREADY_INITIALIZED = 400003, "The PAIG plugin is already initialized"
    PAIG_ACCESS_DENIED = 400004, "{error_message}"
    FRAMEWORKS_NOT_PROVIDED = 400005, "Frameworks are not provided. You should provide at least one framework such as " \
                                      "langchain. You can set to None if you don't want to intercept any framework."
    SHIELD_SERVER_KEY_ID_NOT_PROVIDED = 400006, "Shield server key id is not provided"
    SHIELD_SERVER_PUBLIC_KEY_NOT_PROVIDED = 400007, "Shield server public key is not provided"
    SHIELD_PLUGIN_KEY_ID_NOT_PROVIDED = 400008, "Shield plugin key id is not provided"
    SHIELD_PLUGIN_PRIVATE_KEY_NOT_PROVIDED = 400009, "Shield plugin private key is not provided"
    SHIELD_SERVER_INITIALIZATION_FAILED = 400010, "Shield server initialization failed"

    PROMPT_NOT_PROVIDED = 400011, "Prompt is not provided"
    CONVERSATION_TYPE_NOT_PROVIDED = 400012, "Conversation type is not provided"
    INVALID_APPLICATION_CONFIG_FILE = 400013, "Invalid application config file provided"


    def format(self, **kwargs):
        return super().format(logging.ERROR, **kwargs)


class InfoMessage(BaseMessage):
    """
    Enum that has all the info messages. Do not change the order of the messages. Add new message to the end of the
    list always so that the order is not changed.
    """
    PAIG_IS_INITIALIZED = 200001, "PAIGPlugin initialized with"
    LANGCHAIN_INITIALIZED = 200002, "Langchain setup done with {count} methods intercepted"
    NO_FRAMEWORKS_TO_INTERCEPT = 200003, "No frameworks to intercept"
    PRIVACERA_SHIELD_IS_ENABLED = 200004, "Privacera Shield, enabled={is_enabled}"

    def format(self, **kwargs):
        return super().format(logging.INFO, **kwargs)


class WarningMessage(BaseMessage):
    """
    Enum that has all the warning messages. Do not change the order of the messages. Add new message to the end of the
    list always so that the order is not changed.
    """
    ERROR_MESSAGE_CONFIG_FILE_NOT_FOUND = 300001, "Error message config file not found at {file_path}"
    FRAMEWORK_NOT_SUPPORTED = 300002, "Framework {framework} is not supported"

    def format(self, **kwargs):
        return super().format(logging.WARNING, **kwargs)
