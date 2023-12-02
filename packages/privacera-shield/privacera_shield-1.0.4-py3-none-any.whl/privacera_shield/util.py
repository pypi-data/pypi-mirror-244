import logging
import socket
import threading

from datetime import datetime, timezone
from functools import cache

_logger = logging.getLogger(__name__)


def get_time_now_utc():
    utc_dt = datetime.now(timezone.utc)
    return utc_dt


def get_time_now_utc_str():
    """
    Get current time in UTC in ISO 8601 format compatible with Java
    :return: str
    """
    utc_dt = datetime.now(timezone.utc)
    utc_dt_str = get_time_now_utc().strftime('%Y-%m-%dT%H:%M:%S') + utc_dt.strftime('.%f')[:4] + utc_dt.strftime('Z')
    return utc_dt_str


def get_time_from_isotime(utc_dt_str):
    return datetime.fromisoformat(utc_dt_str)


@cache
def get_my_hostname():
    return socket.gethostname()


@cache
def get_my_ip_address():
    ip_address = ""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
    except Exception:
        _logger.exception("Not able to retrieve host ip address")

    return ip_address


class AtomicCounter:
    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()
        self.max_limit = 2 ** 15 - 1

    def increment(self, offset=1):
        with self._lock:
            self.value = (self.value + offset) % self.max_limit
            return self.value
