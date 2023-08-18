import subprocess

# ADB를 사용하여 현재 실행 중인 앱의 정보 가져오기
adb_output = subprocess.check_output(['adb','shell','dumpsys','window','windows']).decode('utf-8')

# 패키지 이름과 액티비티 이름 추출
current_focus = [line for line in adb_output.split('\n') if 'mCurrentFocus' in line][0]
package_activity = current_focus.split()[-1]
package_name, activity_name = package_activity.split('/')

print("Package Name:", package_name)
print("Activity Name:", activity_name)