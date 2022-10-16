import cv2
from datetime import datetime
from app.core.config import settings
import socket

IP, PORT = settings.WORKER_SERVER
class Manager:
    SAVE_PATH = f"{settings.IMAGE_PATH}/queue/"

    def __init__(self, ws):
        self.ws = ws

    def give_task(self, img):
        name = datetime.now().strftime("%H-%m-%s")
        self.save_img(img, name)
        msg="asdf"
        self.send_task(name)

    def send_task(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((IP, PORT))
            sock.sendall(bytes(msg, 'ascii'))
        pass

    def save_img(self, img, name):
        path = f'{self.SAVE_PATH}/{name}.jpg'
        cv2.imwrite(path, img)
        print(f"저징 완료 {path}")
