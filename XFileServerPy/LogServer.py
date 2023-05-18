from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/log/array", methods=["POST"])
def array_get():
    # 요청 본문에서 JSON 배열 가져오기
    data = request.json

    # 데이터 처리
    for user in data:
        print(user["name"])
        print(user["email"])

    return "Success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)

# 요청 하는쪽 에서 호춯 하기 위한 URL 예.
# url = "http://192.168.60.190:6000/log/array"
