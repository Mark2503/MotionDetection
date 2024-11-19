import os
import threading
import time

import cv2

from config import PHOTO_FOLDER_PATH, ACTIVE_PATH_FOLDER, ACTIVE_SESSIONS_RTSP_FLOW_NAME_FILE, MESSAGE_DETECT_NAME_FILE
from moduls import LogsBot, Modul, Client
from WriteReadJson import WriteReadJson

write_active = WriteReadJson()

sock = Client()


class DetectedRtsp:

    def __init__(self, rtsp):

        self.rtsp = rtsp
        self.video = cv2.VideoCapture(self.rtsp)

        self.date_message = Modul('%Y:%m:%d_%H:%M:%S').set_datetime()
        self.date_file = Modul('%Y-%m-%d_%H-%M-%S').set_datetime()
        self.date_folders = Modul('%Y/%m/%d/%H').set_datetime()
        self.photo_date_paths = Modul(os.path.join(PHOTO_FOLDER_PATH, self.date_folders)).created_folder()
        self.path_file_photo = os.path.join(self.photo_date_paths, f'{self.date_file}_camera{str(rtsp).split("/")[-1][:-2]}.jpeg')
        self.is_active = os.path.join(ACTIVE_PATH_FOLDER, ACTIVE_SESSIONS_RTSP_FLOW_NAME_FILE)
        self.message_detect_file = os.path.join(ACTIVE_PATH_FOLDER, MESSAGE_DETECT_NAME_FILE)

    def running(self):

        try:
            print(self.video)
            self.video.set(3, 1280)  # установка размера окна
            self.video.set(4, 700)

            ret, frame1 = self.video.read()
            ret, frame2 = self.video.read()

            while True:
                time.sleep(1)

                if int(write_active.read_is_active(self.is_active)) == 0:
                    break
                else:
                    # print(self.rtsp)
                    date_message = Modul('%Y:%m:%d_%H:%M:%S').set_datetime()
                    date_file = Modul('%Y-%m-%d_%H-%M-%S').set_datetime()
                    date_folders = Modul('%Y/%m/%d/%H').set_datetime()
                    photo_date_paths = Modul(os.path.join(PHOTO_FOLDER_PATH, date_folders)).created_folder()

                    diff = cv2.absdiff(frame1, frame2)

                    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

                    blur = cv2.GaussianBlur(gray, (5, 5), 0)
                    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

                    dilated = cv2.dilate(thresh, None, iterations=3)

                    сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    for contour in сontours:
                        (x, y, w, h) = cv2.boundingRect(contour)

                        if cv2.contourArea(contour) < 1000:
                            continue

                        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0),
                                      2)  # получение прямоугольника из точек кортежа
                        cv2.putText(frame1, "Status: {}".format("Dvigenie"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255),
                                    3,
                                    cv2.LINE_AA)  # вставляем текст

                        path_file_photo = os.path.join(
                            photo_date_paths, f'{date_file}_camera{str(self.rtsp).split("/")[-1][:-2]}.jpeg')

                        message_detect = f"Время-{date_message}|" \
                                         f"Сервер-{str(self.rtsp).split('/')[2].split('@')[1]}|" \
                                         f"Камера-{str(self.rtsp).split('/')[-1][:-2]}"
                        print(message_detect)
                        # write_active.write_is_active(self.message_detect_file, message_detect)
                        sock.send_message(message_detect)
                        cv2.imwrite(path_file_photo, frame1)

                    # cv2.imshow("frame1", frame1)
                    frame1 = frame2  #
                    ret, frame2 = self.video.read()  #

            self.video.release()
            cv2.destroyAllWindows()

        except Exception as e:
            LogsBot('running').error_logs(e)


def run_detections(param):

    try:

        result = set(value for value in param.values())

        for rtsp in result:
            th_rtsp = threading.Thread(target=DetectedRtsp(str(rtsp)).running)
            th_rtsp.start()

    except Exception as e:
        LogsBot('run_detections').error_logs(e)