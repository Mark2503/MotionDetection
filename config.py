import os

TOKEN_BOT = ""

# ---------------------------------------

USER_ID_NAME_FILE_JSON: str = 'USER_ID.json'

CAMERA_ID_NAME_FILE_JSON: str = 'CAMERA_ID.json'

ACTIVE_SESSIONS_RTSP_FLOW_NAME_FILE: str = 'ACTIVE_RTSP'

MESSAGE_DETECT_NAME_FILE: str = 'message_data'

DETECTIONS_LOG_NAME_FILE: str = "detection.log"

ERRORS_LOG_NAME_FILE: str = 'error.log'

ACCESS_LOG_NAME_FILE: str = 'access.log'

# -----------------------------------

BASE_PATH: str = os.getcwd()

DATA_FOLDER_PATH: str = os.path.join(BASE_PATH, 'Data')

USERS_CAMERA_ACTIVE_FOLDER_PATH: str = os.path.join(DATA_FOLDER_PATH, 'UserCameraActive')

LOGS_FOLDER_PATH: str = os.path.join(DATA_FOLDER_PATH, 'Logs')

ARCHIVE_FOLDER_PATH: str = os.path.join(DATA_FOLDER_PATH, 'Archive')

PHOTO_FOLDER_PATH: str = os.path.join(DATA_FOLDER_PATH, 'Photo')

ACTIVE_PATH_FOLDER: str = os.path.join(DATA_FOLDER_PATH, 'Active')

FOLDERS: list[str] = [
    DATA_FOLDER_PATH, USERS_CAMERA_ACTIVE_FOLDER_PATH,
    LOGS_FOLDER_PATH, ARCHIVE_FOLDER_PATH,
    PHOTO_FOLDER_PATH, ACTIVE_PATH_FOLDER
]