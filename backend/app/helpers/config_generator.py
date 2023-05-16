import os

from dotenv import load_dotenv

_NAME_VAR_ENV = "ENVIRONMENT"
_DEFAULT_ENV = "dev"


class EnvInstaller:

    def __init__(self):
        self.default_path_to_env_config = ".env"
        self.env = os.getenv(_NAME_VAR_ENV, _DEFAULT_ENV)
        if self.env != _DEFAULT_ENV:
            self.default_path_to_env_config += f".{self.env}"
        load_dotenv(self.default_path_to_env_config)
