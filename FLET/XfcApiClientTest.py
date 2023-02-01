import socket


HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))



# 키보드로 입력한 문자열을 서버로 전송하고
# 서버에서 에코되어 돌아오는 메시지를 받으면 화면에 출력합니다.
# quit를 입력할 때 까지 반복합니다.
while True:

    message = input('Enter Message : ')
    if message == 'quit':
    	break

    client_socket.send(message.encode())
    data = client_socket.recv(1024)

    print('Received from the server :',repr(data.decode()))


client_socket.close()