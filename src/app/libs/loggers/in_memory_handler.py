import logging
from collections import deque

log_storage = deque(maxlen=1000)


class InMemoryHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_storage.append(log_entry)
