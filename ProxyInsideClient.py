#!/usr/bin/python
import socket


class ProxyInsideClient:
    def __init__(self):
        self.trans_host = ('127.0.0.1', 9999)
        self.target_host = ('127.0.0.1', 43555)
        self.trans_server = ''
        self.target_server = ''
        self.receive_buff_size = 1024
        self.send_buff_size = 1024

    def init_socket(self):
        self.trans_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        self.target_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        try:
            self.trans_server.connect(self.trans_host)  # 要连接的IP与端口
            self.target_server.connect(self.target_host)  # 要连接的IP与端口
        except Exception as e:
            print("内网客户端socket初始化失败！", e)
            exit(1)
        print("内网客户端初始化成功！")

    def handle_request(self, request):
        return request

    def handle_response(self, response):
        return response

    # 接收报文
    def server_recv(self, sock):
        try:
            buf = sock.recv(self.receive_buff_size)
        except Exception as e:
            print("接收失败！长时间没有来自服务器的请求报文", e)
            exit(2)
        else:
            return buf

    # 发送报文
    def server_send(self, sock, buf):
        try:
            buf_len = sock.send(buf)
        except Exception as e:
            print("发送失败！无法发送请求报文给服务器！", e)
            exit(3)
        else:
            return buf_len

    def run(self):
        # 创建并初始化内网客户端
        self.init_socket()

        # 循环接收处理中转服务器发送的请求报文
        while True:
            # 等待接收中转服务器发送请求报文
            buf = self.server_recv(self.trans_server)

            # 处理请求报文
            buf = self.handle_request(buf)

            # 将请求报文转发给目标服务器
            self.server_send(self.target_server, buf)

            # 等待接收目标服务器发送响应报文
            buf = self.server_recv(self.target_server)

            # 处理响应报文
            buf = self.handle_response(buf)

            # 将响应报文转发给中转服务器
            self.server_send(self.trans_server, buf)


if __name__ == '__main__':
    app = ProxyInsideClient()
    app.run()
