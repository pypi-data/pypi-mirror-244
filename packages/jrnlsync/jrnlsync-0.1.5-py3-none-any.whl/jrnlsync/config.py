from pathlib import Path
from ruamel.yaml import YAML


CONFIG_FOLDER = Path.home() / '.config' / 'jrnlsync'
CONFIG_PATH = CONFIG_FOLDER / 'jrnlsync.yaml'


yaml = YAML()


def read_config(path=None):
    
    # use same configuration folder approach as jrnlsync
    config_path = path or CONFIG_PATH

    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.load(f)
    else:
        # TODO raise config not found error (need to create setup)
        return {}


def create_default_config():
    # create config folder if it doesn't exist
    CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)

    default_jrnl_config_path = Path.home() / '.config' / 'jrnl'

    default_config = {
        "jrnl_folder": str(default_jrnl_config_path.absolute()),
    }
    yaml.dump(default_config, CONFIG_PATH)
