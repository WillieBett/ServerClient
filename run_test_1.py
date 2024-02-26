import subprocess
import time

def send_message(process, message):
    process.stdin.write(message + "\n")
    process.stdin.flush()

def run_test():
    # Start the server in a separate process
    server_process = subprocess.Popen(["python", "server.py", "-port", "8888"])

    # Give some time for the server to start
    time.sleep(2)

    try:
        # Scenario 1: Alice sends a single message
        alice_process = subprocess.Popen(
            ["python", "client.py", "-name", "Alice", "-server_ip", "127.0.0.1", "-port", "8888"],
            stdin=subprocess.PIPE,
            universal_newlines=True,
            text=True,  # Use text mode for input
            bufsize=1,  # Line buffered
        )
        send_message(alice_process, "Hello everyone!")


        # Give some time for Chad and Bob to come online
        time.sleep(5)
       
        bob_process = subprocess.Popen(
            ["python", "client.py", "-name", "Bob", "-server_ip", "127.0.0.1", "-port", "8888"],
            stdin=subprocess.PIPE,
            text=True,  # Use text mode for input
            bufsize=1,  # Line buffered
        )
       

       
        chad_process = subprocess.Popen(
            ["python", "client.py", "-name", "Chad", "-server_ip", "127.0.0.1", "-port", "8888"],
            stdin=subprocess.PIPE,
            text=True,  # Use text mode for input
            bufsize=1,  # Line buffered
        )
       
        


        
        # Scenario 2: Alice, Bob, and Chad are online
            

        # Give some time for clients to come online
        time.sleep(2)

        # Bob sends a message to all
        send_message(bob_process, "Hello everyone!")

        # Give some time for the message to propagate
        time.sleep(5)
        

        # Scenario 3: Alice sends a message to all
        send_message(alice_process, "Hi everyone!")

        # Give some time for the message to propagate
        time.sleep(5)

        # Scenario 4: Doug joins the server (not part of the group)
        doug_process = subprocess.Popen(
            ["python", "client.py", "-name", "Doug", "-server_ip", "127.0.0.1", "-port", "8888"],
            stdin=subprocess.PIPE,
            text=True,  # Use text mode for input
            bufsize=1,  # Line buffered
        )

        # Wait for Doug to join
        doug_process.wait()
    finally:
        # Terminate all processes
        server_process.terminate()
        alice_process.terminate()
        bob_process.terminate()
        chad_process.terminate()
        doug_process.terminate()

if __name__ == "__main__":
    run_test()
