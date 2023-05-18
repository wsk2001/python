# -*- coding: utf-8 -*-

"""
flask 를 이용한 rest api server 예제
"""

from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    # 데이터 수신
    json_string = request.get_json()
    pretty_json = json.dumps(json_string, indent=4)

    # 데이터 출력
    print(pretty_json)

    return "Success"

# flask default port is 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

