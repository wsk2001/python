import socket
import requests
import subprocess
import psutil

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print("Hostname:", hostname)
print("IP Address:", ip_address)
print("\n\n");


ip = requests.get('https://api.ipify.org').text
print('My public IP address is:', ip)
print("\n\n");



result = subprocess.run(["netstat", "-na"], stdout=subprocess.PIPE)
#output = result.stdout.decode("utf-8")

print(result)
print("\n\n");


for conn in psutil.net_connections(kind='inet'):
    if conn.status == 'ESTABLISHED':
        print(conn)
print("\n\n");

