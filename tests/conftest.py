import json
import os
import socket
import subprocess
import sys
import time
import uuid

import pytest
import zmq

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_DIR, "sab.db")


def uid():
    """random suffix so every run uses fresh usernames/numbers"""
    return uuid.uuid4().hex[:6]


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def remove_db():
    for suffix in ("", "-journal", "-wal", "-shm"):
        path = DB_PATH + suffix
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


class PhoneBookClient:
    """minimal zmq REQ client, equivalent to client.py, used to talk to server.py"""

    def __init__(self, ip, port, proc=None):
        self.ip = ip
        self.port = port
        self.proc = proc

    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def send(self, commands, timeout_ms=4000):
        """send a command list and normalize the reply.

        Returns dict:
          responses: list of {"command_name", "result"} or None
          error:     raw error text / timeout description or None
          raw:       unmodified reply
        """
        ctx = zmq.Context.instance()
        sock = ctx.socket(zmq.REQ)
        sock.setsockopt(zmq.LINGER, 0)
        sock.setsockopt(zmq.RCVTIMEO, timeout_ms)
        sock.setsockopt(zmq.SNDTIMEO, timeout_ms)
        sock.bind(f"tcp://{self.ip}:{self.port}")
        try:
            sock.send_json(commands)
            try:
                raw = sock.recv_json()
            except zmq.Again:
                return {"responses": None, "error": "timeout: no response from server", "raw": None}
        finally:
            sock.close(0)

        if isinstance(raw, list):
            return {"responses": raw, "error": None, "raw": raw}
        if isinstance(raw, str):
            try:
                data = json.loads(raw)
            except ValueError:
                return {"responses": None, "error": raw, "raw": raw}
            if isinstance(data, list):
                return {"responses": data, "error": None, "raw": raw}
            return {"responses": None, "error": str(data), "raw": raw}
        return {"responses": None, "error": repr(raw), "raw": raw}


def run_cmd(client, command_name, timeout_ms=4000, **params):
    """send a single command wrapped in the standard request format"""
    return client.send([{"command_name": command_name, "parameters": params}], timeout_ms)


def assert_server_survives(client, timeout_ms=1500):
    """after an error, the spec requires the server to keep serving requests"""
    r = run_cmd(client, "get_all_phone_users", timeout_ms=timeout_ms)
    assert r["responses"] is not None, (
        f"server stopped responding after the error (process alive={client.alive()}, reply={r['error']!r})"
    )


def start_server(ip, port):
    proc = subprocess.Popen(
        [sys.executable, "-u", os.path.join(PROJECT_DIR, "server.py"), "--ip", ip, "--port", str(port)],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        line = proc.stdout.readline()
        if "ready" in line.lower():
            return proc
        if proc.poll() is not None:
            raise RuntimeError("server exited during startup:\n" + proc.stdout.read())
    proc.kill()
    raise RuntimeError("server did not become ready within 15 seconds")


@pytest.fixture(scope="session")
def server():
    """one shared server for the whole session, started on a clean database"""
    remove_db()
    port = free_port()
    proc = start_server("127.0.0.1", port)
    yield PhoneBookClient("127.0.0.1", port, proc)
    proc.kill()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


@pytest.fixture()
def lonely_server():
    """a dedicated server per test, used by negative tests that may kill it"""
    port = free_port()
    proc = start_server("127.0.0.1", port)
    yield PhoneBookClient("127.0.0.1", port, proc)
    proc.kill()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass
