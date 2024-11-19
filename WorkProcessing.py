import time

from moduls import LogsBot
from WriteReadJson import WriteReadJson
from config import CAMERA_ID_NAME_FILE_JSON, USER_ID_NAME_FILE_JSON


class WorkProcessing:

    def __init__(self):
        pass

    # Возвращает все rtsp потоки
    def run_read_camera_id(self):

        write_read_json = WriteReadJson()

        try:

            result = write_read_json.read_json_file(CAMERA_ID_NAME_FILE_JSON)
            yield set(list(result.values()))

        except Exception as e:
            LogsBot(name='WorkProcessing().run_read_camera_id()').error_logs(e)

    def run_read_user_id(self):

        try:
            write_read_json = WriteReadJson()

            result = write_read_json.read_json_file(USER_ID_NAME_FILE_JSON)

            for key in result.keys():
                return int(key)

        except Exception as e:
            LogsBot(name='WorkProcessing().run_read_user_id').error_logs(e)
