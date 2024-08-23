"""
This logging solution uses a decorator combined with a `LogConfig` object to 
provide customized logging for methods in a Python class. Here's how it works:

1. **LogConfig Object**: A `LogConfig` class encapsulates logging instructions, 
    including custom messages (`before_msg`, `after_msg`) and additional data 
    (`before_data`, `after_data`) to be logged before and after a method is executed.

2. **Decorator**: The `log_event` decorator accepts a `CollisionLogger` 
    instance and a `LogConfig` object. It wraps the target method, executing 
    the logging instructions specified in the `LogConfig` before and after the 
    method runs.

3. **Method Decoration**: Methods are decorated with `@log_event`, passing the 
    appropriate `LogConfig` object. This setup automatically handles logging 
    without cluttering the method logic.

4. **Custom Logging**: When a method is executed, if logging is enabled 
    (`debug=True`), the decorator logs customized messages and data before and 
    after the method’s core logic, based on the configurations provided in the 
    `LogConfig`.
"""

import logging
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler and set the level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)


class LogConfig:
    """
    Configuration for logging events.
    """

    def __init__(
        self,
        before_msg: str = None,
        after_msg: str = None,
        before_data: dict = None,
        after_data: dict = None,
    ):
        self.before_msg = before_msg
        self.after_msg = after_msg
        self.before_data = before_data or {}
        self.after_data = after_data or {}


def log_event(config: LogConfig, debug: bool = True) -> Callable:
    """
    Decorator to log events with the given config.

    Parameters
    ----------
    config : LogConfig
        The configuration for the logging event.
    debug : bool, optional
        Whether to log the event in debug mode, by default False.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            debug = kwargs.get("debug", True)
            obj = args[1] if len(args) > 1 else None
            obj_desc = obj.description() if obj else ""
            method_name = func.__name__

            if debug:
                if config.before_msg:
                    custom_before_msg = config.before_msg.format(
                        method_name=method_name, object_desc=obj_desc
                    )
                    logger.debug(
                        custom_before_msg,
                        {**config.before_data, "Args": args, "Kwargs": kwargs},
                    )

            result = func(*args, **kwargs)

            if debug:
                if config.after_msg:
                    custom_after_msg = config.after_msg.format(
                        method_name=method_name, object_desc=obj_desc
                    )
                    logger.debug(
                        custom_after_msg,
                        {
                            **config.after_data,
                            "Result": result,
                            "Args": args,
                            "Kwargs": kwargs,
                        },
                    )

            return result

        return wrapper

    return decorator
