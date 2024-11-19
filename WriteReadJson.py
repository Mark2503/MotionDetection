import json
import os

from moduls import LogsBot
from config import USERS_CAMERA_ACTIVE_FOLDER_PATH, ACTIVE_PATH_FOLDER, ACTIVE_SESSIONS_RTSP_FLOW_NAME_FILE


class WriteReadJson:

    def __init__(self):
        pass

    # Метод записи
    def __write_file(self, name_file, date):

        try:

            with open(name_file, 'w', encoding='UTF-8') as file:
                file.write(f'{date}')

        except Exception as e:
            LogsBot('WriteReadJson().__write_file').error_logs(e)

        # Метод записи

    def __read_file(self, name_file):

        try:

            with open(name_file, 'r', encoding='UTF-8') as file:
                num = file.read()
                return num

        except Exception as e:
            LogsBot('WriteReadJson().__read_file').error_logs(e)

    # Метод читает файл json
    def read_json_file(self, namefile: str) -> dict:
        """
        :param namefile:
        :return:
        """
        try:
            path_file: str = os.path.join(USERS_CAMERA_ACTIVE_FOLDER_PATH, namefile)
            #print(path_file)
            if os.path.isfile(path_file):
                with open(path_file, 'r', encoding='utf-8') as file:
                    data = file.read()

                    if len(data) == 0:
                        # LogsBot('read_json_file-[{}]').access_logs('успех')
                        return {}

                    else:
                        # LogsBot(f'read_json_file-[{dict(json.loads(data))}]').access_logs('успех')
                        #print(dict(json.loads(data)))
                        return dict(json.loads(data))

            else:
                file = open(path_file, 'w', encoding='UTF-8')
                file.close()
                LogsBot('read_json_file-[файл создан]').access_logs('успех')
                return {}

        except Exception as e:
            LogsBot('read_json_file-[ошибка]').error_logs(e)

    # Записывает данные в json file
    def write_json_file(self, namefile: str, *args) -> str:
        """
        :param namefile:
        :param args:
        :return:
        """

        try:

            path_file_json: str = os.path.join(USERS_CAMERA_ACTIVE_FOLDER_PATH, namefile)

            data = {args[0]: {'id': args[0], 'username': args[2], 'first_name': args[1], 'last_name': args[3]}}

            data_json: dict = self.read_json_file(namefile)

            if data_json.get(str(args[0])) is None:

                data_json.update(data)

                with open(path_file_json, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(data_json))
                    LogsBot('write_json_file-[Вы добавлены в систему]').access_logs('успех')
                    return 'Вы добавлены в систему'

            else:
                LogsBot('write_json_file-[Вы уже есть в системе]').access_logs('успех')
                return 'Вы уже есть в системе'

        except Exception as e:
            LogsBot('write_json_file-[ошибка]').error_logs(e)

    # Записывает данные по rtsp в json файл
    def rtsp_write_json(self, namefile: str, rtsp: str):

        try:
            path_file_json: str = os.path.join(USERS_CAMERA_ACTIVE_FOLDER_PATH, namefile)

            data_json: dict = self.read_json_file(namefile)
            num = len(data_json) + 1

            data_json.update({num: rtsp})

            with open(path_file_json, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data_json))

            LogsBot('rtsp_write_json-[Видео поток добавлен в систему]').access_logs('успех')
            return 'Видео поток добавлен в систему'

        except Exception as e:
            LogsBot('rtsp_write_json-[ошибка]').error_logs(e)

    # Метод читает файл Active
    def read_is_active(self, is_active):

        try:

            return self.__read_file(is_active)

        except Exception as e:
            pass

    # Метод записывает в файл Active
    def write_is_active(self, is_active, param):

        try:

            self.__write_file(is_active, param)

        except Exception as e:
            pass
