import socket
import os
import time

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()
# 设置端口号
port = 9999
# 连接服务，指定主机和端口
s.connect((host, port))
while True:
    msg = input('>>:').strip()
    os.system("clear")
    s.send(msg.encode('utf-8'))
    msg = s.recv(1024)
    print (msg.decode('utf-8'))