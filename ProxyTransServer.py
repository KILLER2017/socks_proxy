#!/usr/bin/env python
# coding:utf-8
import socket


class ProxyTransServer:
    def __init__(self):
        self.trans_host = ('127.0.0.1', 9999)
        self.target_host = ('127.0.0.1', 43555)
        self.socket_listen_limit = 5
        self.trans_server = ''
        self.inside_client = ''
        self.inside_address = ''
        self.receive_buff_size = 1024
        self.send_buff_size = 1024

    def init_socket(self):
        self.trans_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.trans_server.bind(self.trans_host)
        except Exception as e:
            print('中转服务器创建失败！', e)
            exit(1)
        print('中转服务器创建成功！')
        # 设置操作系统可以挂起的最大连接数量，该值至少为1
        self.trans_server.listen(self.socket_listen_limit)

    def accept_client_connect(self):
        self.inside_client, self.inside_address = self.trans_server.accept()
        print("内网客户端已连接...", self.inside_address)

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
        # 创建并初始化中转服务器
        self.init_socket()
        # 监听，等待内网客户端连接
        self.accept_client_connect()

        while True:
            # 等待外网用户连接
            outside_client, outside_address = self.trans_server.accept()
            print('外网用户连接...', outside_address)

            # 接收外网用户请求报文
            buf = self.server_recv(outside_client)

            # 处理请求报文
            buf = self.handle_request(buf)

            # 将请求报文转发给内网客户端
            self.server_send(self.inside_client, buf)

            # 接收内网客户端响应报文
            buf = self.server_recv(self.inside_client)

            # 处理响应报文
            buf = self.handle_response(buf)

            # 将响应报文转发给外网用户
            self.server_send(outside_client, buf)

            # 关闭和外网用户之间的连接
            print("关闭和外网用户之间的连接")
            outside_client.close()


if __name__ == '__main__':
    app = ProxyTransServer()
    app.run()
