import grpc
import chat_pb2
import chat_pb2_grpc
import threading
import time
import logging

# Configure the logging settings
logging.basicConfig(
    filename='client.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ChatClient:
    def __init__(self, username, server_ip, port):
        self.username = username
        self.server_ip = server_ip
        self.port = port
        self.received_messages = []
        self.channel = grpc.insecure_channel(f'{server_ip}:{port}')
        self.stub = chat_pb2_grpc.ChatStub(self.channel)

    def send_message(self, message):
        request = chat_pb2.MessageRequest(sender=self.username, content=message)
        response = self.stub.SendMessage(request)
        print(f"Server response: {self.username}-> {response.status} ")
        logging.info(f"Server response: {self.username}-> {response.status} ")



    def receive_messages(self):
        request = chat_pb2.ClientInfo(username=self.username)
        responses = self.stub.ReceiveMessages(request)
        for response in responses:
            time.sleep(1)
            if hasattr(response, 'content') and hasattr(response, 'sender'):
                print(f"\nReceived from {response.sender}: {response.content}")
                logging.info(f"\nReceived from {response.sender}: {response.content}")

            else:
                print(f"Received message does not have expected fields.")
                logging.warning("Received message does not have expected fields.")

                
            self.received_messages.append(response)

    def check_for_messages(self):
        while True:
            time.sleep(1)
            if self.received_messages:
                print("\nNew Messages:")
                logging.info("New messages")
                for message in self.received_messages:
                    print(f"{message.sender}: {message.content}")
                    logging.debug(f"{message.sender}: {message.content}")

                self.received_messages = []

def interactive_send(client_instance):
    while True:
        try:
            message = input("Enter your message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_instance.send_message(message)
        except EOFError:
            logging.warning("End of file error")
            break

def receive_messages_display(client_instance):
    while True:
        client_instance.receive_messages()
        time.sleep(2)
        if client_instance.received_messages:
            print("\nNew Messages:")
            for message in client_instance.received_messages:
                print(f"{message.sender}: {message.content}")
            client_instance.received_messages = []

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chat client")
    parser.add_argument("-name", type=str, help="Client username", required=True)
    parser.add_argument("-server_ip", type=str, help="Server IP address", required=True)
    parser.add_argument("-port", type=int, help="Server port number", required=True)
    args = parser.parse_args()

    # Create a single instance of ChatClient
    client_instance = ChatClient(args.name, args.server_ip, args.port)

    time.sleep(5)

    # Start the client threads with the shared instance of ChatClient
    send_thread = threading.Thread(target=interactive_send, args=(client_instance,))
    receive_thread = threading.Thread(target=receive_messages_display, args=(client_instance,))

    receive_thread.start()
    send_thread.start()


    # Wait for threads to finish
    receive_thread.join()
    send_thread.join()
    
