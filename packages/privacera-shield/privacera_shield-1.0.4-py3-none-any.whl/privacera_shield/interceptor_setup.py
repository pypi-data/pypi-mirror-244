import logging

from .langchain_callback import LangChainLLMInterceptorSetup
from .message import InfoMessage, WarningMessage

_logger = logging.getLogger(__name__)

def setup(paig_plugin):
    for framework in paig_plugin.get_frameworks_to_intercept():
        if framework.lower() == 'langchain':
            langchain_interceptor = LangChainLLMInterceptorSetup()
            langchain_interceptor.find_all_methods_to_intercept()
            count = langchain_interceptor.setup_interceptors(paig_plugin)
            if _logger.isEnabledFor(logging.INFO):
                _logger.info(InfoMessage.LANGCHAIN_INITIALIZED.format(count=count))
        elif framework.lower() == 'none':
            _logger.info(InfoMessage.NO_FRAMEWORKS_TO_INTERCEPT.format())
        else:
            _logger.warning(WarningMessage.FRAMEWORK_NOT_SUPPORTED.format(framework=framework))


