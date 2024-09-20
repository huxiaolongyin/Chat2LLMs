import os
from dotenv import load_dotenv


load_dotenv(override=True)


def load_str_env(name: str, required: bool = False) -> str:
    """
    Load environment variable as string
    :param name: name of the environment variable
    :param required: whether the environment variable is required
    """
    if os.environ.get(name):
        return os.environ.get(name)

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

    if required:
        raise Exception(f"Env {name} is not set")


class Config:
    """Backend configuration"""

    def __init__(self):
        from __init__ import __VERSION__

        self.VERSION = __VERSION__
        self.DB_SQLITE_PATH = load_str_env("DB_SQLITE_PATH", required=True)

        # web
        self.WEB_ROUTE_PREFIX = "/api/v1"

        # OLLAMA
        self.OLLAMA_HOST = load_str_env("OLLAMA_HOST", required=True)
        self.OLLAMA_URL = load_str_env("OLLAMA_URL", required=True)

        # QRANT
        self.QRANT_HOST = load_str_env("QRANT_HOST", required=True)
        self.QRANT_PORT = load_int_env("QRANT_PORT", required=True)

        self.EMBEDDING_MODEL_PATH = load_str_env("EMBEDDING_MODEL_PATH", required=True)

        # WETHER
        self.API_KEY = load_str_env("API_KEY", required=True)

        # MYSQL
        self.DB_MYSQL_USER = load_str_env("DB_MYSQL_USER", required=True)
        self.DB_MYSQL_PASSWORD = load_str_env("DB_MYSQL_PASSWORD", required=True)
        self.DB_MYSQL_HOST = load_str_env("DB_MYSQL_HOST", required=True)
        self.DB_MYSQL_PORT = load_int_env("DB_MYSQL_PORT", required=True)
        self.DB_MYSQL_DATABASE = load_str_env("DB_MYSQL_DATABASE", required=True)

CONFIG = Config()
