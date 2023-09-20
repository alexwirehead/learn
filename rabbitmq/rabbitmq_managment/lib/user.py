from lib import http_client
from lib import mod_logger

logger = mod_logger()


class UsersAdmin:
    def __init__(self):
        self.__http_client = http_client.HttpClient()
        self.__api_users_uri = '/api/users/'

    def __check_user_existence(self, username: str) -> bool:
        uri = self.__api_users_uri + username
        resp = self.__http_client.call_api(method='GET',
                                           api_playload=None,
                                           api_uri=uri)
        if resp.status_code == 200 and resp.json():
            return True
        return False

    def create_user(self, username: str, password: str,  tags: str) -> None:
        user_existence = self.__check_user_existence(username=username)
        if user_existence:
            logger.error(f'Пользователь с именем {username} уже существует')
            exit(0)
        playload = {"password": password,
                    "tags": tags}
        uri = self.__api_users_uri + username
        resp = self.__http_client.call_api(method='PUT',
                                           api_playload=playload,
                                           api_uri=uri)
        if resp.status_code == 201:
            logger.info(f'Создан пользователь {username}')
        else:
            logger.info(f'Ошибка при создании пользователя. HTTP CODE: {resp.status_code} '
                        f'Body-ответа: {resp.text if resp.text else None}')

    def delete_user(self, username: str):
        uri = self.__api_users_uri + username
        resp = self.__http_client.call_api(method='DELETE',
                                           api_uri=uri,
                                           api_playload=None)
        logger.info(resp.text, resp.content, resp.status_code)

    def modify(self, username: str):
        pass
