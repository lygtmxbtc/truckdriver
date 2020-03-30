import socket
import os
import threading
import time
import queue


"""
generate game code
"""
GAME_BEGIN = False
PLAYER_LIST = []
CURRENT_TURN_PLAYER = None
PLAYER_ACT = queue.Queue()
"""
create socket code
"""
# 创建 socket 对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()
port = 9999
# 绑定端口号
serversocket.bind((host, port))
# 设置最大连接数，超过后排队
serversocket.listen(5)

def process(clientsocket, addr):
    print("connect from " + str(addr))
    while True:
        # 这里用于与客户端交互数据
        data = clientsocket.recv(1024).decode('utf-8')
        print (data)
        if not GAME_BEGIN:
            clientsocket.sendall(
                ("current play number: %s\nwait for more player join..."
                 % len(PLAYER_LIST)).encode('utf-8')
            )
        else:
            # 游戏开始
            # 接收玩家客户端操作
            if clientsocket == CURRENT_TURN_PLAYER:
                PLAYER_ACT.put(data)
            else:
                clientsocket.sendall("it is not your turn".encode('utf-8'))

# 同步游戏
def synchronize_game(data):
    data_utf = data.encode('utf-8')
    for player in PLAYER_LIST:
        player[0].sendall(data_utf)

# 等待玩家加入服务器
while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()
    t = threading.Thread(target=process, args=(clientsocket, addr))
    t.start()
    PLAYER_LIST.append((clientsocket, addr))
    if len(PLAYER_LIST) == 2:
        break

print(PLAYER_LIST)
print("GAME START")
# 初始化游戏
# 同步游戏副本到玩家客户端
synchronize_game("map info")
time.sleep(0.5)
synchronize_game("card info")
GAME_BEGIN = True

# 游戏开始 从第一个玩家开始循环回合
while True:
    for player in PLAYER_LIST:
        CURRENT_TURN_PLAYER = player[0]
        CURRENT_TURN_PLAYER.sendall("itsyourturn".encode('utf-8'))
        # act1 移动
        action = PLAYER_ACT.get()
        print(action)
        synchronize_game("act1 result")
        # act2 买入卖出换牌
        action = PLAYER_ACT.get()
        print(action)
        synchronize_game("act2 result")
        # act3 补牌
        time.sleep(0.5)
        synchronize_game("act3 result")


