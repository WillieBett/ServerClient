# ServerClient
Rpc Communication

Description
You will implement a simple client-server “group chat” system with a n-clients/1-server configuration. Let’s say Alice, Bob and Chad (the three client processes) wants to talk to each other. Alice sends a message to the server, and when Bob and Chad is online, they connect to the server and download the “unread” messages. Your program should allow the clients to send/receive messages from the server. The server keeps track of the clients that has received the messages and only sends the unread messages.

Implementation
You can use whatever programming languages you wish. But unless there is a strong reason not to, please use gRPC as your framework (it does support quite a few languages).

You will need a server program (e.g., server.py) that spawns the server process. For example, this will spawn the server on port XXXX:

$ python server.py -port XXXX
You will also implement a client program (e.g. client.py) that will spawn the client process.

For example, this will spawn the client process with username Luis, connects and registers with the server.

$ python client.py -name Luis -server_ip <ipaddress> -port <port>
The client can then send a message along with its id to the server.

Note that multiple clients can enter the same name, but their messages should not get confused.

You must use asynchronous RPC for all communications between the clients and server. This includes connecting to the server, and sending/receiving messages from the server.

Testing
You will provide multiple test cases for your system as driver-test program (e.g., run_test_1.py). The program will spawn the client and server process, and send/receive messages. Sample scenarios to test:

“Alice sends a single message. Chad and Bob comes online after a 5 second delay, and receives all messages from Alice. (Log the message in the console)
“Alice, Bob, and Chad are online. Bob sends a message to all, Chad and Alice receives the message (The sender Bob doesnt receive the message from the server). Alice sends a message to all, Bob and Chad receives it (but not Alice). Doug, not part of the group, joins the server but receives no message.
Please put appropriate print statements.

Packaging your application
Package your application using docker. You should submit a Dockerfile that will create a container. The docker file will create an image that will have the necessary environment for running the test case. Basically, it will pull an image from the repository, copy your code, and execute the test files. When the docker container is deployed, it will automatically run all the test cases. Submit the Dockerfile as part of your assignment.
