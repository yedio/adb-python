import time
import datetime
import os
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

# 초기값
signup_name = "seokyeju"
signup_pw = "testPW2023"
target_date_year = 2008
target_date_month = 12
target_date_day = 12


def prepare_screenshot_directory():
    # ./res/screenshot 폴더가 존재하는 경우 삭제
    screenshot_dir = "./res/screenshot"
    if os.path.exists(screenshot_dir):
        print("스크린샷 폴더 삭제")
        for filename in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"파일 삭제 오류: {e}")

    # ./res/screenshot 폴더 생성
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        print("스크린샷 폴더 생성")


def calculateSimilarity(image_path):
    # 스크린샷 캡쳐 path 설정
    current_time = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"/sdcard/pic_screenshot_{current_time}.png"
    screenshot_path_pc = f"./res/screenshot/pic_screenshot_{current_time}.png"

    # screencap 명령을 사용하여 화면 캡처
    capture_command = f"screencap {screenshot_path}"
    device.shell(capture_command)
    time.sleep(2)
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
    print(f"유사도: {similarity}")

    if similarity >= 95:
        positions = (button_center_x, button_center_y)
        time.sleep(2)
        device.shell(f"input tap {positions[0]} {positions[1]}")
        print(f"클릭했습니다. {positions[0]} {positions[1]}")
        return True
    else:
        print("유사한 값이 아닙니다.")
        return False

def dragDateItem(start_image):
    # 스크린샷 캡쳐 path 설정
    current_time = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"/sdcard/pic_screenshot_{current_time}.png"
    screenshot_path_pc = f"./res/screenshot/pic_screenshot_{current_time}.png"

    # screencap 명령을 사용하여 화면 캡처
    capture_command = f"screencap {screenshot_path}"
    device.shell(capture_command)
    time.sleep(2)
    device.pull(screenshot_path, screenshot_path_pc)

    image1 = cv2.imread(screenshot_path_pc)
    image2 = cv2.imread(start_image)

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
    print(f"유사도: {similarity}")

    current_date = datetime.datetime.now()


    if similarity >= 94:
        positions = (button_center_x, button_center_y)
        time.sleep(1)

        # 년도 설정
        # input swipe xSource, ySource, xDestination, yDestination, Duration
        gap_year = current_date.year - target_date_year
        year_count = 0
        while True:
            if (year_count < abs(gap_year)):
                device.shell(f"input swipe {positions[0]} {positions[1]} {positions[0]} {positions[1] + 150} 300")
                year_count += 1
                time.sleep(1)
                continue
            else:
                print("end: year")
                break

        # 월 설정
        gap_month = current_date.month - target_date_month
        month_count = 0
        while True:
            if (month_count < abs(gap_month)):
                if(gap_month > 0):
                    device.shell(f"input swipe {positions[0] + 200} {positions[1]} {positions[0] + 200} {positions[1] + 150} 300")
                elif (gap_month < 0):
                    device.shell(f"input swipe {positions[0] + 200} {positions[1]} {positions[0] + 200} {positions[1] - 150} 300")
                month_count += 1
                time.sleep(1)
            else:
                print("end: month")
                break

        # 일 설정
        gap_day = current_date.day - target_date_day
        day_count = 0
        while True:
            if (day_count < abs(gap_day)):
                if (gap_day > 0):
                    device.shell(f"input swipe {positions[0] + 350} {positions[1]} {positions[0] + 350} {positions[1] + 150} 300")
                elif (gap_day < 0):
                    device.shell(f"input swipe {positions[0] + 350} {positions[1]} {positions[0] + 350} {positions[1] - 150} 300")
                day_count += 1
                time.sleep(1)
            else:
                print("end: day")
                break



prepare_screenshot_directory()

# [가입하기 버튼 클릭]
while True:
    if calculateSimilarity("./res/pic_signup.png"):
        break
    else:
        continue
time.sleep(2)

# [팝업 x]
device.shell("input keyevent 4")
time.sleep(2)

# [input name]
device.shell(f"input text {signup_name}")
time.sleep(2)

# [click enter]
device.shell("input keyevent 66")
time.sleep(2)

# [input passward (limit len 6)]
device.shell(f"input text {signup_pw}")
time.sleep(2)

# [image 다음 - pic_next_button.png]
calculateSimilarity("./res/pic_next_button.png")
time.sleep(2)

# [image 나중에 - pic_later_savelogin.png]
calculateSimilarity("./res/pic_later_savelogin.png")
time.sleep(2)

# [drag 날짜 설정]
dragDateItem("./res/pic_signup_startdate_year.png")
for _ in range(2):
    device.shell("input keyevent 22")
    time.sleep(1)
device.shell("input keyevent 66")
time.sleep(2)


# [image 다음 - pic_next_button.png]
calculateSimilarity("./res/pic_next_button.png")
time.sleep(2)

# [image 다음 - pic_next_button.png]
calculateSimilarity("./res/pic_next_button.png")
time.sleep(2)