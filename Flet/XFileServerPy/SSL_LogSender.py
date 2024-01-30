import requests
import json
import urllib3

# 에러가 나는 urllib3 에서 insecureRequestWarning 메세지를 예외처리(except)하는 방법
# 아래는 https 인증 관련 대처 방법임.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Server URL and header
# url = "http://192.168.60.190:6000/log/array"
url = "https://192.168.60.190:6000/log/array"
headers = {"Content-Type": "application/json"}

def send_json_request(url, json_data):
    # Create a secure HTTP request.
    
    if url.startswith("https"): # 요청 보내기 (https 일 경우)
        response = requests.post(url, json=json_data, verify=False)
    
    else: # 요청 보내기 (http 일 경우)
        response = requests.post(url, headers=headers, data=json.dumps(json_data))

    return response.status_code

if __name__ == "__main__":
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

    # Send the JSON data to the server.
    status_code = send_json_request(url, data)

    # 응답 확인
    if status_code == 200:
        print("Log 전송 성공")
    else:
        print("Log 전송 실패")
