import zmq
from datetime import datetime
import time

def subscription_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 5000)

    connected = False

    while True:
        try:
            socket.connect("tcp://tunnel.srcserver.xyz:6660")
            # 发送消息到云服务器
            socket.send_string("amount")

            # 等待服务器的回复
            amount=int(socket.recv_string())
            if amount!=0:
                socket.send_string("get")
                # 接收并打印服务器发送的消息
                message = socket.recv_string()
                # 获取当前时间
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 打印消息接收的时间和内容
                print(f"Received message at {current_time}: {message}")

        except zmq.ZMQError as e:
            # 如果之前已经连接，打印错误信息
            print(f"网络连接出错：{e}")

        time.sleep(1)  # 等待一秒钟再尝试重新连接

if __name__ == "__main__":
    subscription_client()
