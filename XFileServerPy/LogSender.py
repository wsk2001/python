import requests
import json

# 샘플 JSON 배열 생성
data = [
    {
        "name": "John Doe",
        "email": "johndoe@example.com"
    },
    {
        "name": "Jane Doe",
        "email": "janedoe@example.com"
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
