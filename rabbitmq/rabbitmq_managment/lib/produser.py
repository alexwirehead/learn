import pika

from lib import (RABBIT_HOST,
                 RABBIT_PORT,
                 RABBIT_USERNAME,
                 RABBIT_PASSWORD,
                 mod_logger)

logger = mod_logger()

class RQProducer:
    def __init__(self, queue_name: str):
        self.__queue_name = queue_name

    def __enter__(self):
        credentials = pika.PlainCredentials(username=RABBIT_USERNAME,
                                            password=RABBIT_PASSWORD)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST,
                                                                            port=RABBIT_PORT,
                                                                            credentials=credentials))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def __check_queue(self) -> None:
        channel = self.connection.channel()
        channel.queue_declare(queue=self.__queue_name, durable=True, passive=True)

    def publish_msg(self, body: str) -> None:
        try:
            self.__check_queue()
            channel = self.connection.channel()
            channel.basic_publish(exchange='', routing_key=self.__queue_name, body=body)
            logger.info(f'Сообщение "{body}" отправлено')
        except pika.exceptions.ChannelClosedByBroker as e:
            logger.error(f'Возникла ошибка при отправке сообщения: {e}')
