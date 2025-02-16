import zmq
from datetime import datetime
import threading

message_queue=[]

def send_monitor(monitor_socket):
    global message_queue
    while True:
        command=monitor_socket.recv_string()
        if command=="amount":
            reply_message=str(len(message_queue))
        elif command=="get":
            reply_message=message_queue.pop(0)
        monitor_socket.send_string(reply_message)


if __name__ == "__main__":
    context = zmq.Context()
    publisher = context.socket(zmq.REP)
    publisher.bind("tcp://0.0.0.0:6660")  # 使用不同的端口进行发布

    t=threading.Thread(target=send_monitor,args=(publisher,))
    t.start()

    responder = context.socket(zmq.REP)
    responder.bind("tcp://0.0.0.0:6661")  # 保持原始端口用于处理客户端请求

    print("Cloud Server is listening...")


    while True:
        # 等待客户端消息
        message = responder.recv_string()
        # 假设这里只是简单地回复消息
        reply_message = "Received"
        responder.send_string(reply_message)

        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 打印消息接收的时间和内容
        print(f"Received message at {current_time}: {message}")

        message=f"{current_time}: {message}"

        message_queue.append(message)
