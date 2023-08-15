import socket
import sys, time
import json

def send_server(msg):
    UDP_IP_ADDRESS = "192.168.60.190"
    UDP_PORT_NO = 20001

    # Create a socket for sending data to the server
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the message to the server
    clientSock.sendto(msg.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))

    # Close the socket
    clientSock.close()


def main(argv):
    user_name = "wonsool"
    client_ip = "192.168.60.190"
    os_name = "Windows 10"
    client_type = "API"
    mode = "E"
    dt = "2023-08-03 12:33:48.361"
    strFileName = "/home/wonsool/IQFile/test/enc/data07/data_5128.txt"
    fileSize = "127736"
    hashcode = "6887e03db9e82b5fcd749c279f282817aa357367a990b3a8bb98cdec449669c5"
    duration = "0.004"
    status = "Success"

    msg = "[{"
    msg += "\"userId\":\"" + user_name + "\"";  
    msg += ",\"accIp\":\"" + client_ip + "\"";  
    msg += ",\"enpIp\":\"" + client_ip + "\"";  
    msg += ",\"agtEnpPlatform\":\"" + os_name + "\"";  
    msg += ",\"agtType\":\"" + client_type + "\"";  
    msg += ",\"jobOperation\":\"" + mode + "\"";  
    msg += ",\"agtDate\":\"" + dt + "\"";  
    msg += ",\"agtFilename\":\"" + strFileName + "\"";  
    msg += ",\"agtFilesize\":" + fileSize;  
    msg += ",\"agtFilehash\":\"" + hashcode + "\"";  
    msg += ",\"agtDuration\":" + duration;  
    msg += ",\"agtResult\":\"" + status + "\"";                  
    msg += "}]"

    send_server(msg)

if __name__ == "__main__":
    main(sys.argv)
