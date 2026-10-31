from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger

from anyio.functools import lru_cache

from app.libs.loggers.in_memory_handler import InMemoryHandler


@lru_cache(maxsize=None)
def get_logger(name: str) -> Logger:
    logger: Logger = getLogger(name)

    logger.setLevel(DEBUG)
    logger.propagate = False

    formatter = Formatter("%(asctime)s - %(name)s[%(process)d] - %(levelname)s - %(message)s")

    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # ile_handler = RotatingFileHandler(
    #     filename="logs/app.log",
    #     mode="a",
    #     maxBytes=5 * 1024 * 1024,
    #     backupCount=3,
    #     encoding="utf-8",
    # )
    # ile_handler.setLevel(DEBUG)
    # ile_handler.setFormatter(formatter)
    # logger.addHandler(ile_handler)
    #

    # memory_handler = InMemoryHandler()
    #
    # memory_handler.setLevel(DEBUG)
    # memory_handler.setFormatter(formatter)
    # logger.addHandler(memory_handler)

    return logger
