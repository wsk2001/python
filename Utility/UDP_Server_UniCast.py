import socket
import sys, time
import json


def main(argv):
    localIP = "0.0.0.0"
    localPort = 20001
    bufferSize = 1024 * 1024

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    # Listen for incoming datagrams
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        # receive data
        json_string = bytesAddressPair[0].decode("utf-8")
        json_object = json.loads(json_string)
        pretty_json = json.dumps(json_object, indent=4)

        clientMsg = "Message from Client:{}".format(pretty_json)
        clientIP = "Client IP Address:{}".format(bytesAddressPair[1])
        print(clientMsg)
        print(clientIP)


if __name__ == "__main__":
    main(sys.argv)
