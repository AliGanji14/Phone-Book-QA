"""Client-side tests — TC-C-* cases mapped in docs/02_test_cases.md"""
import os
import subprocess
import sys

import pytest

from conftest import PROJECT_DIR, free_port

CLIENT = os.path.join(PROJECT_DIR, "client.py")
SAMPLES = os.path.join(PROJECT_DIR, "samples")


def run_client(args, timeout=20):
    return subprocess.run(
        [sys.executable, "-u", CLIENT] + args,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def test_client_file_not_found():
    r = run_client(["--ip", "127.0.0.1", "--port", str(free_port()),
                    "--file", os.path.join(SAMPLES, "does_not_exist.json")])
    assert "does not exist" in r.stdout, f"stdout was: {r.stdout!r}"


def test_client_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{ this is not json", encoding="utf-8")
    r = run_client(["--ip", "127.0.0.1", "--port", str(free_port()), "--file", str(bad)])
    assert "Invalid json file" in r.stdout, f"stdout was: {r.stdout!r}"


def test_client_sends_valid_file_and_prints_response(server):
    r = run_client(["--ip", "127.0.0.1", "--port", str(server.port),
                    "--file", os.path.join(SAMPLES, "commands.json")])
    assert "Response is" in r.stdout, f"stdout was: {r.stdout!r}"
    assert server.alive(), "server died while serving the real client"


def test_client_hangs_when_server_unreachable():
    # documented defect: client.py waits forever on recv_json when no server answers
    port = free_port()
    with pytest.raises(subprocess.TimeoutExpired):
        run_client(["--ip", "127.0.0.1", "--port", str(port),
                    "--file", os.path.join(SAMPLES, "commands.json")], timeout=6)
