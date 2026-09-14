## SERVER SIDE

you can run server.py with command:

    python3 server.py --port 7878 --ip 127.0.0.1

default value of port is 9090 and default value of ip is 127.0.0.1

server waits until a message is received by client


## CLIENT SIDE

you can run client.py with command:

    python3 client.py --port 7878 --ip 127.0.0.1 --file sample/commands.json

default value of port is 9090 and default value of ip is 127.0.0.1 and default value of file is sample/commands.json

client sends a json file to server and waits for response

## SAMPLES

there is a samples directory that contains several json file for test 
    