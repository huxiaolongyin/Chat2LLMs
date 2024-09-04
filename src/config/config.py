import os
import sys
from dotenv import load_dotenv


dotenv_path = "D:/code/chat2LLMs/.env"
load_dotenv(dotenv_path=dotenv_path)
default_env_values = {"SERVICE_PORT": 8000}


def load_str_env(name: str, required: bool = False) -> str:
    """
    Load environment variable as string
    :param name: name of the environment variable
    :param required: whether the environment variable is required
    """
    if os.environ.get(name):
        return os.environ.get(name)

    if default_env_values.get(name) is not None:
        return default_env_values.get(name)

    if required:
        raise Exception(f"Env {name} is not set")


def load_int_env(name: str, required: bool = False) -> int:
    """
    Load environment variable as int
    :param name: name of the environment variable
    :param required: whether the environment variable is required
    """
    if os.environ.get(name):
        return int(os.environ.get(name))

    if default_env_values.get(name) is not None:
        return default_env_values.get(name)

    if required:
        raise Exception(f"Env {name} is not set")


class Config:
    """Backend configuration"""

    def __init__(self):
        from __init__ import __VERSION__

        self.VERSION = __VERSION__
        self.SERVICE_PORT = load_int_env("SERVICE_PORT", required=True)
        self.DB_SQLITE_PATH = load_str_env("DB_SQLITE_PATH", required=True)

        # web
        self.WEB_ROUTE_PREFIX = "/api"


CONFIG = Config()
