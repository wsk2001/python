from flask import Flask, request
import json
import time
from threading import Thread
import ssl

app = Flask(__name__)

json_data = ''

@app.route("/log/array", methods=["POST"])
def array_get():
    global json_data
    json_data = request.json
    print(json_data)

    return "Success"

@app.route("/")
def index():
    return 'Web App with Python Flask!'


def view_data():
  global json_data

  while True:
    # data parsing
    cnt = 0
    for user in json_data:
        print()
        print(user["userId"])
        print(user["accIp"])
        print(user["enpIp"])
        print(user["agtEnpPlatform"])
        print(user["agtType"])
        print(user["jobOperation"])
        print(user["agtDate"])
        print(user["agtFilename"])
        print(user["agtFilesize"])
        print(user["agtFilehash"])
        print(user["agtDuration"])
        print(user["agtResult"])
        cnt = 1
    if 0 < cnt:
        json_data = ''
    time.sleep(1)


if __name__ == "__main__":
    thread = Thread(target=view_data, daemon=True)
    thread.start()
    
    use_protocol = "https"

    if use_protocol.startswith("https"):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        ssl_context.load_cert_chain(certfile='cert_py_log_server.pem', keyfile='key_py_log_server.pem', password='password')
        app.run(host='0.0.0.0', port=6000, ssl_context=ssl_context)
    else:
        app.run(host='0.0.0.0', port=6000)

# An example URL for calling on the requesting side.
# url = "https://192.168.60.190:6000/log/array"
# openssl req -x509 -newkey rsa:2048 -keyout key_py_log_server.pem -out cert_py_log_server.pem -days 365
# password