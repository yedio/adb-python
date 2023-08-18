import time
from ppadb.client import Client as AdbClient
import cv2

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

def calculateSimilarity(image_path):
    # 이미지 파일을 로드
    screenshot_path = "/sdcard/pic_screenshot.png"
    screenshot_path_pc = "./res/pic_screenshot.png"

    # screencap 명령을 사용하여 화면 캡처
    capture_command = f"screencap /sdcard/screenshot.png"

    # screencap 명령을 사용하여 화면 캡처
    device.shell(capture_command)
    time.sleep(5)
    device.pull(screenshot_path, screenshot_path_pc)

    image1 = cv2.imread(screenshot_path_pc)
    image2 = cv2.imread(image_path)

    # cv2.matchTemplate()를 사용하여 유사도 맵 계산
    result = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)

    # 유사도 맵에서 유사도 값 얻기
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 유사도 값을 0.1부터 1로 변환하여 반환
    similarity = (max_val - 0.1) / 0.9  # 범위를 0.1~1로 조정
    similarity = max(0.1, min(1, similarity))  # 범위를 0.1~1로 제한
    similarity = int(similarity * 100)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 클릭할 좌표 계산 (중심 위치)
    button_center_x = max_loc[0] + image2.shape[1] // 2
    button_center_y = max_loc[1] + image2.shape[0] // 2

    if similarity >= 95:
        positions = (button_center_x, button_center_y)

        return similarity, positions
    else:
        return similarity, (0,0)

while True:
    # 유사도 계산
    similarity, xy = calculateSimilarity("./res/pic_signup.png")
    print("Normalized ", similarity, xy)
    if similarity >= 95:
        time.sleep(2)
        print(xy, xy[0], xy[1])
        device.shell(f"input tap {xy[0]} {xy[1]}")
        print("클릭했습니다.")
        break
    else:
        print("유사한 값이 아닙니다.")
        continue