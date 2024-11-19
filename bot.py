import os
import shutil
import time

import telebot
from telebot import types

from config import TOKEN_BOT, CAMERA_ID_NAME_FILE_JSON, USER_ID_NAME_FILE_JSON, \
    PHOTO_FOLDER_PATH, ACTIVE_PATH_FOLDER, LOGS_FOLDER_PATH, ARCHIVE_FOLDER_PATH, ACTIVE_SESSIONS_RTSP_FLOW_NAME_FILE, \
    MESSAGE_DETECT_NAME_FILE

from moduls import LogsBot, Modul, Server
from WriteReadJson import WriteReadJson
from DetectionMotion import run_detections

bot = telebot.TeleBot(TOKEN_BOT)

write_read_json = WriteReadJson()

server = Server()

is_Active = 0


@bot.message_handler(commands=['start', 'help'])
def start(message):

    text_message = str(message.text).split('@')[0]

    try:

        if text_message == '/start':

            bot.send_message(message.chat.id, text='Добро пожаловать нажмите - /help')

            LogsBot(name='start-[пользователь нажал /start]').access_logs('успех')

        elif text_message == '/help':

            bot.send_message(message.chat.id, text='/add_camera - добавить номер камеры\n'
                                                   '/GetId - получить id для отправки уведомлений\n'
                                                   '/GetID_Group - получить id отправки уведомлений в группу\n'
                                                   '/run_detected - запуск обнаружения\n'
                                                   '/download_detection_archive - выгрузить архив с фото обнаружения\n'
                                                   '/download_logs - выгрузить логи\n'
                                                    )

            LogsBot(name='start-[пользователь нажал /help]').access_logs('успех')

    except Exception as e:
        LogsBot(name='help-[ошибка нажатие /start или /help]').error_logs(e)
        return e


@bot.message_handler(commands=['add_camera'])
def add_camera(message):

    text_message = str(message.text).split('@')[0]

    if text_message == '/add_camera':

        try:
            users_id = {message.from_user.id}
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_language: list = [types.KeyboardButton('192.168.3.252'), types.KeyboardButton('192.168.3.253')]
            markup.add(*button_language)

            text: str = 'Выберите сервер'
            bot.send_message(message.chat.id, text, reply_markup=markup)
            bot.register_next_step_handler(message, choice_server, users_id)
            LogsBot(name='add_camera-[пользователь нажал /add_camera]').access_logs('успех')

        except Exception as e:
            LogsBot(name='add_camera-[ошибка нажатие /add_camera]').error_logs(e)


# Выбор сервера
def choice_server(message, *args):
    try:

        if message.from_user.id in args[0]:

            ip_server = message.text
            bot.send_message(message.chat.id, text='Введите номер камеры: ')
            bot.register_next_step_handler(message, add_rtsp_cam, args[0], ip_server)
            LogsBot(name=f'choice_server-[{ip_server}]').access_logs('успех')

    except Exception as e:
        LogsBot(name='choice_server-[ошибка]').error_logs(e)


# Добавление камеры
def add_rtsp_cam(message, *args):

    try:

        if message.from_user.id in args[0]:

            number = [str(i) for i in range(0, 101)]

            if message.text in number:

                rtsp: str = f'rtsp://admin:192168102Abc@{args[1]}:554/ISAPI/Streaming/Channels/{message.text}02'
                result = write_read_json.rtsp_write_json(CAMERA_ID_NAME_FILE_JSON, rtsp=rtsp)
                bot.send_message(message.chat.id, text=result)
                LogsBot(name=f'add_rtsp_cam-[{result}]').access_logs('успех')
            else:

                bot.send_message(message.chat.id, text='Ошибка нажмите на - /add_camera')
                LogsBot(name=f'add_rtsp_cam-[]').error_logs("ошибка добавления")

    except Exception as e:
        LogsBot(name='add_rtsp_cam-[ошибка]').error_logs(e)


@bot.message_handler(commands=['GetId'])
def get_id_user(message):
    text_message = str(message.text).split('@')[0]

    if text_message == '/GetId':

        result: str = write_read_json.write_json_file(
            USER_ID_NAME_FILE_JSON,
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.username,
            message.from_user.last_name
        )

    bot.send_message(message.chat.id, text=result)


@bot.message_handler(commands=['GetID_Group'])
def get_id_group(message):

    text_message = str(message.text).split('@')[0]

    if text_message == '/GetID_Group':
        result: str = write_read_json.write_json_file(
            USER_ID_NAME_FILE_JSON,
            message.chat.id,
            message.chat.title,
            'None',
            'None'
        )
        bot.send_message(message.chat.id, text=result)


@bot.message_handler(commands=['download_detection_archive'])
def download_detection_archive(message):

    text_message = str(message.text).split('@')[0]

    if text_message == '/download_detection_archive':

        try:

            archive_name = os.path.join(ARCHIVE_FOLDER_PATH, Modul('%Y-%m-%d_%H').set_datetime())

            shutil.make_archive(archive_name, 'zip', PHOTO_FOLDER_PATH)

            file = open(f'{archive_name}.zip', 'rb')

            bot.send_document(message.chat.id, file)

        except Exception as e:
            LogsBot('download_detection_archive').error_logs(e)


@bot.message_handler(commands=['download_logs'])
def download_logs(message):

    text_message = str(message.text).split('@')[0]

    if text_message == '/download_logs':

        try:

            archive_name = os.path.join(ARCHIVE_FOLDER_PATH, 'logs')

            shutil.make_archive(archive_name, 'zip', LOGS_FOLDER_PATH)

            file = open(f'{archive_name}.zip', 'rb')

            bot.send_document(message.chat.id, file)

        except Exception as e:

            LogsBot('download_logs').error_logs(e)


@bot.message_handler(commands=['run_detected'])
def run_detected(message):

    global is_Active


    is_active = os.path.join(ACTIVE_PATH_FOLDER, ACTIVE_SESSIONS_RTSP_FLOW_NAME_FILE)
    text_message = str(message.text).split('@')[0]
    message_detect = os.path.join(ACTIVE_PATH_FOLDER, MESSAGE_DETECT_NAME_FILE)
    try:

        if text_message == '/run_detected':

            if is_Active == 0:
                is_Active = 1

                write_read_json.write_is_active(is_active, is_Active)
                run_detections(write_read_json.read_json_file(CAMERA_ID_NAME_FILE_JSON))

            else:

                is_Active = 0
                write_read_json.write_is_active(is_active, is_Active)

                bot.send_message(message.chat.id, text='Процесс остановлен для запуска нажните - /run_detected')
        while True:
            time.sleep(1)

            if is_Active == 0:
                break

            else:

                conn, addr = server.listen().accept()
                print('connected:', addr)
                text = conn.recv(1024)
                print(str(text, 'utf-8'))
                for i in [int(i) for i in write_read_json.read_json_file(USER_ID_NAME_FILE_JSON).keys()]:
                    bot.send_message(chat_id=i, text=str(text, 'utf-8'))

        conn.close()

    except Exception as e:
        LogsBot('run_detected').error_logs(e)


s = {'database_name': {'table_name': {
    'id': [1],
    'users': ['mark']
}}}