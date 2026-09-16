"""Non-functional tests (the 2 optional cases allowed by the assignment)"""
import time

from conftest import run_cmd, uid


def test_response_time_simple_query(server):
    """TC-S-31: a simple query must be answered in less than 2 seconds"""
    t0 = time.perf_counter()
    r = run_cmd(server, "get_all_phone_users")
    elapsed = time.perf_counter() - t0
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert elapsed < 2.0, f"simple query took {elapsed:.2f}s (limit 2s)"


def test_bulk_add_30_contacts(server):
    """TC-S-32: adding 30 contacts in one request must complete in less than 3 seconds"""
    commands = [
        {
            "command_name": "add_phone_user",
            "parameters": {
                "username": f"bulk{i}_{uid()}",
                "phone_number": f"0930{i:08d}",
                "explanation": "bulk test",
            },
        }
        for i in range(30)
    ]
    t0 = time.perf_counter()
    r = server.send(commands)
    elapsed = time.perf_counter() - t0
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert len(r["responses"]) == 30
    assert elapsed < 3.0, f"bulk add of 30 contacts took {elapsed:.2f}s (limit 3s)"
