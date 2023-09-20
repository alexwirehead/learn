from lib import (http_client,
                 mod_logger
                 )

logger = mod_logger()


class QueuesAdmin:
    def __init__(self):
        self.__http_client = http_client.HttpClient()
        self.__api_queues_uri = '/api/queues/%2F/'

    def create_queue(self, queue_name: str, queue_args: dict) -> None:
        uri = self.__api_queues_uri + queue_name
        playload = {"auto_delete": False,
                    "durable": True,
                    "arguments": queue_args,
                    "node": "rabbit@test-rabbit"}

        resp = self.__http_client.call_api(method='PUT', api_playload=playload, api_uri=uri)
        if resp.status_code == 201:
            logger.info(f'Очередь {queue_name} успешно создана')
        else:
            logger.error(f'Ошибка при создании очереди HTTP Code: {resp.status_code} ответ API: {resp.text}')

    def delete_queue(self, queue_name: str):
        pass

