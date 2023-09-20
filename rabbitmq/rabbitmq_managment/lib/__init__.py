from pathlib import Path
from sys import stdout
from typing import Any

import yaml
from loguru import logger

CONFIG_FILE_NAME = 'client_config.yml'


def mod_logger() -> logger:
    logger.remove()
    logger.add(stdout,
               format="{level} {module}-{function} {message}",
               diagnose=True, colorize=True, level="INFO")

    return logger

def fetch_config_data(config_key: str, config_file_name: str) -> Any:
    """
    Функция чтения конфиг файла
    :param config_key -- имя ключа из конфиг-файла
    :return: config -- данные из yml-конфиг файла
    """
    logger = mod_logger()
    path_to_config = Path(__file__).resolve().parent / config_file_name
    logger.debug(path_to_config)

    try:
        with open(path_to_config, encoding='utf-8') as cf:
            config = yaml.load(cf, Loader=yaml.FullLoader)
            logger.debug(f'Конфиг файл {config_file_name} успешно открыт')
    except FileNotFoundError:
        logger.error(f'Конфиг-файл {config_file_name} не существует')
    try:
        config_data = config[config_key]
        logger.debug(f'Данные для ключа {config_key} успешно получены')
        return config_data
    except KeyError:
        logger.error(f'Ключа {config_key} в конфиге {config_file_name} не существует')


RABBIT_HOST = fetch_config_data('rabbit_connection', CONFIG_FILE_NAME)['host']
RABBIT_PORT = fetch_config_data('rabbit_connection', CONFIG_FILE_NAME)['port']

RABBIT_API_PORT = fetch_config_data('rabbit_connection', CONFIG_FILE_NAME)['api_port']
RABBIT_ROOT_API_URL = f'http://{RABBIT_HOST}:{RABBIT_API_PORT}'

RABBIT_USERNAME = fetch_config_data('rabbit_creds', CONFIG_FILE_NAME)['username']
RABBIT_PASSWORD = fetch_config_data('rabbit_creds', CONFIG_FILE_NAME)['password']





