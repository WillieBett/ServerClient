import grpc
import chat_pb2
import chat_pb2_grpc
import threading
import time
import concurrent.futures
import logging

# Configure logging settings
logging.basicConfig(
    filename='server.log',  # Specify the log file
    level=logging.DEBUG,      # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s]: %(message)s',  # Define the log message format
    datefmt='%Y-%m-%d %H:%M:%S')  # Specify the date format

class ChatServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.clients = {}

    def SendMessage(self, request, context):
        sender = request.sender
        message = request.content 
        for client in self.clients.values():
            if sender != client.username:
                client.receivedMessages.append(f"{sender}: {message}")
        return chat_pb2.MessageResponse(status="Message sent successfully")
    logging.info( "Message sent successfully")

    def ReceiveMessages(self, request, context):
        username = request.username
        if username not in self.clients:
            self.clients[username] = request

        for message in self.clients[username].receivedMessages:
            response_stream = chat_pb2.Message(content=message)
            yield response_stream
        logging.info("Message Received successfully")


def server(port):
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server listening on port {port}")
    logging.info(f"Server listening on port {port}")
    try:
        while True:
            time.sleep(86400)  # 1 day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chat server")
    parser.add_argument("-port", type=int, help="Port number", required=True)
    args = parser.parse_args()
    server(args.port)
