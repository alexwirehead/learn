import argparse
from textwrap import dedent

from lib import (mod_logger,
                 user,
                 rq_queue,
                 produser)

logger = mod_logger()


def create_user(username: str, password: str, tags: str) -> None:
    users_admin = user.UsersAdmin()
    users_admin.create_user(username=username,
                            password=password,
                            tags=tags)


def delete_user(username: str) -> None:
    users_admin = user.UsersAdmin()
    users_admin.delete_user(username=username)


def create_queue(queue_name: str, queue_args: dict) -> None:
    queue_admin = rq_queue.QueuesAdmin()
    queue_admin.create_queue(queue_name=queue_name,
                             queue_args=queue_args)


def publish_msg(message_body: str, queue_name: str):
    with produser.RQProducer(queue_name=queue_name) as pd:
        pd.publish_msg(body=message_body)


def run_command(args, parser):
    commands = args
    rq_object = commands.object
    if rq_object == 'user' and commands.username and commands.user_password and commands.tags:
        create_user(username=commands.username,
                    password=commands.user_password,
                    tags=commands.tags)
    elif rq_object == 'queue' and commands.queue_name:
        create_queue(queue_name=commands.queue_name,
                     queue_args=commands.args_queue)
    elif rq_object == 'msg' and commands.msg_queue_name and commands.body_msg:
        publish_msg(message_body=commands.body_msg,
                    queue_name=commands.msg_queue_name)
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Скрипт управления RabbitMQ',
                                     usage=dedent('''\
                                     Примеры использования
                                        Вызов стправки:
                                            rq_admin.py -h
                                        Создание пользователя:
                                            rq_admin.py -o user -u foo -p bar -t management
                                        
                                        Создание очереди:
                                            rq_admin.py -o queue -q new_queue -a {}
                                        
                                        Отправка сообщения:
                                            rq_admin.py -o msg -mq new_queue -b 'Hello World!'
                                        '''
                                                  ),
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-o', '--object',
                        action='store',
                        choices=['user', 'queue', 'msg'],
                        required=True,
                        help='Объект RabbitMQ с которым производится действие')

    users = parser.add_argument_group('Аргументы для администирования пользователей')
    users.add_argument('-u', '--username',
                       dest='username',
                       help='Имя пользователя')
    users.add_argument('-p', '--password',
                       dest='user_password',
                       help='Пароль пользователя')
    users.add_argument('-t', '--tags',
                       dest='tags',
                       choices=['administrator', 'monitoring', 'management'],
                       help='Тэги пользователя')

    queue = parser.add_argument_group('Опции для администирования очередей')
    queue.add_argument('-q', '--queue-name',
                       dest='queue_name',
                       help='Имя очереди')
    queue.add_argument('-a', '--args-queue',
                       dest='args_queue',
                       required=False,
                       default={},
                       help='Опции очереди')

    msg = parser.add_argument_group('Аргументы для отправки сообщения в очередь')
    msg.add_argument('-mq', '--msg-queue-name',
                     dest='msg_queue_name',
                     help='Имя очереди для отправи сообщения')
    msg.add_argument('-b', '--body-msg',
                     dest='body_msg',
                     help='Тело сообщения')

    args = parser.parse_args()
    run_command(args, parser)
