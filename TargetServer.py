#!/usr/bin/python
import socket
import datetime


target_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
target_server.bind(('127.0.0.1', 43555))
print("目标服务器已启动！")
target_server.listen(5)
client, address = target_server.accept()
while True:
    print('等待来自代理客户端的请求报文......')
    buf = client.recv(1024)
    print(buf)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在

    sendMsg = "HTTP/1.1 200 OK\r\n\r\nHello World ---- " + nowTime
    print(sendMsg)
    client.send(sendMsg.encode())
    print('发送响应报文给代理客户端')

client.close()