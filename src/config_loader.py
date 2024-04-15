import yaml
from pathlib import Path


def load_config(config_file: Path) -> dict:
    """
    Load the configuration file
    :param config_file: path to the configuration file
    :return: dict
    """
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


config = load_config(Path(__file__).parent.parent / 'config.yaml')
