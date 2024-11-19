import os
import socket
import datetime

from config import LOGS_FOLDER_PATH, ACCESS_LOG_NAME_FILE, ERRORS_LOG_NAME_FILE, DETECTIONS_LOG_NAME_FILE


class Modul:

    def __init__(self, params: str) -> str:

        self.param = params

    # Метод создает папки
    def created_folder(self):

        try:

            if os.path.exists(self.param):
                LogsBot(name=f'run_bot-[папка существует: {self.param}]').access_logs('успех')
                return self.param

            else:
                os.makedirs(self.param)
                LogsBot(name=f'run_bot-[папка создана: {self.param}]').access_logs('успех')
                return self.param

        except Exception as e:
            LogsBot(name=f'run_bot-[ошибка: {self.param}]').error_logs(e)
            return e

    def set_datetime(self):

        try:

            return datetime.datetime.now().strftime(self.param)

        except Exception as e:
            LogsBot(name='set_datetime-[ошибка создания папки]').error_logs(e)
            return e


class LogsBot:

    def __init__(self, name: str = ''):

        self.name: str = name
        self.folder_logs: str = LOGS_FOLDER_PATH

    # Метод записи логов
    def __write_log(self, name_file, params):

        try:

            with open(name_file, 'a', encoding='UTF-8') as file:
                file.write(f'{params}\n')

        except Exception as e:
            return e

    # Метод логирования доступа
    def access_logs(self, access):

        try:

            data_text: str = f"{self.name}-{Modul('%Y:%m:%d_%H:%M:%S').set_datetime()}-{access}"
            file_access_log_path: str = os.path.join(self.folder_logs, ACCESS_LOG_NAME_FILE)

            self.__write_log(name_file=file_access_log_path, params=data_text)

        except Exception as e:
            return e

    # Метод логирования ошибок
    def error_logs(self, error):

        try:
            data_text: str = f"{self.name}-{Modul('%Y:%m:%d_%H:%M:%S').set_datetime()}-{error}"
            file_error_log_path: str = os.path.join(self.folder_logs, ERRORS_LOG_NAME_FILE)

            self.__write_log(name_file=file_error_log_path, params=data_text)

        except Exception as e:
            return e

    # Метод логирования обнаружения
    def detection_log(self, param: str):

        try:

            file_error_log_path: str = os.path.join(self.folder_logs, DETECTIONS_LOG_NAME_FILE)

            self.__write_log(name_file=file_error_log_path, params=param)

        except Exception as e:
            return e


class Server:

    def __init__(self, port: int = 5000):

        self.port: int = port
        self.ip: str = socket.gethostbyname(socket.gethostname())

    def listen(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(10)
        return sock


class Client:

    def __init__(self, port: int = 5000):
        self.port: int = port
        self.ip: str = socket.gethostbyname(socket.gethostname())

    def send_message(self, message):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        sock.send(bytes(message, encoding='UTF-8'))


