from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/log/array", methods=["POST"])
def array_get():
    data = request.json
    print(data)

    # data parsing
    for user in data:
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

    return "Success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)

# An example URL for calling on the requesting side.
# url = "http://192.168.60.190:6000/log/array"
