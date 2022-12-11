import configparser
from os.path import expanduser


def config(group: str,
           key: str) -> str:
    """
    Get credentials from pyconfig.cfg file in your home directory. If environment variable DI_ANALYTICS_ENVIRONMENT is defined, use this to read from Databricks secrets scope.

    Args:
        group: Group string in config file.
        key: Key string in config file.

    Returns:
        Configuration value.

    Raises:
        OSError: If we are unable to read from ~/pyconfig.cfg file.
        NoOptionError: When configuration value is missing from ~/pyconfig.cfg file.

    """

    cfg: configparser.ConfigParser = configparser.ConfigParser()
    try:
        cfg.read(expanduser("~") + '/pyconfig.cfg')
    except OSError:
        print('an error occurred while trying to read ~/pyconfig.cfg file.')
    try:
        return cfg.get(group, key)

    except configparser.NoOptionError:
        print('configuration value missing from ~/pyconfig.cfg.')
