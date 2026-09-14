import json
import optparse
import os
import time
from json import JSONDecodeError

import zmq

from core.errors import ValidationFailure, ApplicationError


def tcp_client(ip, tcp_port, command_file):
    """send a json file on tcp ip:port

    Args:
        ip (str): ip
        tcp_port (int): port
        command_file (str): path to json file
    """
    ctx = zmq.Context()
    s = ctx.socket(zmq.REQ)

    s.bind(f"tcp://{ip}:{tcp_port}")
    print(f"Client is sending data on tcp://{ip}:{tcp_port}...")
    if not os.path.exists(command_file):
        raise ValidationFailure("Json file does not exist.")
    with open(command_file) as json_file:
        try:
            data = json.load(json_file)
        except JSONDecodeError as err:
            raise ValidationFailure("Invalid json file")
    print("Data is valid to send...")
    s.send_json(data)
    print("Data is sent to server...")
    time.sleep(1)
    msg = s.recv_json()
    print(f"Response is \n{msg}")


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option("--port", type="int", dest="port", default=9090, help="port number")
    parser.add_option("--file", type="str", dest="file", default="samples/commands.json", help="path to json file")
    parser.add_option("--ip", type="str", dest="ip", default='127.0.0.1', help="ip")
    # parser.add_option("--log-level", type="string", dest="log_level", default='info', help="logging level")
    (options, args) = parser.parse_args()

    port = 9090
    if options.port in range(1000, 9998):
        port = options.port
    try:
        tcp_client(options.ip, port, options.file)
    except ApplicationError as err:
        print(err)
    except Exception as err:
        raise err
