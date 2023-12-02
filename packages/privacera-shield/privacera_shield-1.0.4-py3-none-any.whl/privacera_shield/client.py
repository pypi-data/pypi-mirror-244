from . import core


class APIKeyProvider:
    """
    Interface for providing an API key.
    """

    def get_key(self):
        """
        Get the application key.

        Returns:
            str: The application key.
        """
        pass


def setup(**options):
    """
    This function initializes the PAIGPlugin instance and calls its 'init' method to set up the PAIG plugin.

    Note:
        The global '_paig_plugin' variable is used to store the PAIGPlugin instance for later use.

    """
    core.setup(**options)


def create_shield_context(**kwargs):
    return core.create_shield_context(**kwargs)


def set_current_user(username):
    """
    Set the current user_name context for the PAIG plugin.

    Args:
        username (str): The username of the current user_name.

    Note:
        This function sets the user_name context using the 'set_current_user_context' method of the PAIGPlugin instance
        stored in the global '_paig_plugin' variable.

    """
    core.set_current_user(username)  # Set the current user_name


def set_current(**kwargs):
    """
    Set the list of name-value pairs from kwargs into the thread-local context for the PAIG plugin.
    :param kwargs:
    :return:
    """
    core.set_current(**kwargs)


def get_current_user():
    """
    Get the current user_name context for the PAIG plugin.
    :return:
    """
    return core.get_current("username")


def get_current(key, default_value=None):
    """
    Get the value of the given key from the thread-local context for the PAIG plugin.
    :param key:
    :param default_value:
    :return:
    """
    return core.get_current(key, default_value)


def clear():
    """
    Clear the thread-local context for the PAIG plugin.
    :return:
    """
    core.clear()


def check_access(**kwargs):
    return core.check_access(**kwargs)

def dummy_access_denied():
    core.dummy_access_denied()