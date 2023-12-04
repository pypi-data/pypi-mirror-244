import logging
import time
from typing import Any, Callable, Tuple, Type, Union

logging_logger = logging.getLogger(__name__)


def retryx(
    retry_on: Union[Type[Exception], Tuple[Type[Exception], ...]],
    max_retries: int = 2,
    backoff_factor: int = 1,
    logger: logging.Logger = logging_logger,
):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def retry_internal(*args: Any, **kwargs: Any) -> Any:
            for n in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    if n == max_retries:
                        if logger is not None:
                            logger.error(f"{e}, Exhausted Retries!!!!!!")
                        raise e
                    seconds = backoff_factor * (2 ** (n - 1))
                    time.sleep(seconds)
                    if logger is not None:
                        logger.info(f"Retrying attempt {n}.... in {seconds}")
                except Exception as e:
                    raise e

        return retry_internal

    return decorator
