# coding:utf-8
import time
import datetime
from socket import *
from multiprocessing import Process

from SpiderClient.settings import http


def talk(conn, addr):
    print("子进程开始.")
    message = None
    while 1:
        try:
            start_time = time.time()
            start_time = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
            message = conn.recv(1024)
            print(message)
            http.request(r'client_update', {'message': message, 'ip': addr[0],
                                            'status': 'True', 'start_time': start_time})
            # 启动
            if not message: break
            conn.send(message.upper())
        except Exception:
            # 中断
            http.request(r'client_update', {'message': message, 'status': 'False'})
            break


if __name__ == '__main__':
    server = socket()
    ip_port = ("127.0.0.1", 8080)
    server.bind(ip_port)
    server.listen(5)
    while 1:
        conn, client_addr = server.accept()
        print(conn, client_addr)
        p = Process(target=talk, args=(conn, client_addr))
        p.start()