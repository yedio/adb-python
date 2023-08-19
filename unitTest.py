import time
import os
from ppadb.client import Client as AdbClient
import cv2
import datetime


# LDPlayer 에뮬레이터의 IP 주소와 포트
emulator_ip = "127.0.0.1"
emulator_port = 5037

# ADB 연결
client = AdbClient(emulator_ip, emulator_port)
devices = client.devices()
print(devices)

if len(devices) == 0:
    exit()

device = devices[0]

package_name = "com.instagram.android"
activity_name = "com.instagram.mainactivity.MainActivity"

device.shell(f"am start -n {package_name}/{activity_name}")

print("start")

# unit test 시작
