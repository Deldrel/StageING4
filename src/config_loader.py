import yaml
from pathlib import Path


class ConfigLoader:
    _config = None

    @classmethod
    def load_config(cls, config_file: Path) -> dict:
        """
        Load the configuration file
        :param config_file: path to the configuration file
        :return: dict
        """
        if cls._config is None:
            with open(config_file, 'r') as f:
                cls._config = yaml.safe_load(f)
        return cls._config


config = ConfigLoader.load_config(Path(__file__).parent.parent / 'config.yaml')
