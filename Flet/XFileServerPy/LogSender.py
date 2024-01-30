import requests
import json

data = [
    {
        "userId":"testuser",
        "accIp": "192.168.60.190",
        "enpIp": "192.168.60.190",
        "agtEnpPlatform": "windows 10",
        "agtType": "LA",
        "jobOperation": "E",
        "agtDate": "2023-05-18 12:23:37.123",
        "agtFilename": "C:\\Temp\\test1.cpp",
        "agtFilesize": 100,
        "agtFilehash": "12345678901234567890123456789012",
        "agtDuration": 120.34,
        "agtResult": "success"
    },
    {
        "userId":"testuser",
        "accIp": "192.168.60.190",
        "enpIp": "192.168.60.190",
        "agtEnpPlatform": "windows 10",
        "agtType": "LA",
        "jobOperation": "E",
        "agtDate": "2023-05-18 12:23:37.123",
        "agtFilename": "C:\\Temp\\test2.cpp",
        "agtFilesize": 100,
        "agtFilehash": "12345678901234567890123456789012",
        "agtDuration": 120.34,
        "agtResult": "success"
    }
]

# JSON 배열을 요청 본문으로 전달하는 POST 요청 생성
url = "http://192.168.60.190:6000/log/array"
headers = {"Content-Type": "application/json"}

# 요청 보내기
response = requests.post(url, headers=headers, data=json.dumps(data))

# 응답 확인
if response.status_code == 200:
    print("요청 성공")
else:
    print("요청 실패")
