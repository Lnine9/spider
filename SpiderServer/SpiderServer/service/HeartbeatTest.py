# coding:utf-8
import time
from socket import *


client = socket()
ip_port = ("127.0.0.1", 8080)
client.connect(ip_port)
while 1:

    inp = '1pc'
    if not inp: continue
    client.send(inp.encode("utf-8"))
    from_server_msg = client.recv(1024)
    print("来自服务端的消息:", from_server_msg)
    time.sleep(5)

client.close()