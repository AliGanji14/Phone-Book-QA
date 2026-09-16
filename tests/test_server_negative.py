"""Negative server tests — each test gets its own server because these cases
are expected to expose crash defects. Spec requirement: the server must answer
with a structured {"command_name", "result"} error and keep running."""
import pytest

from conftest import assert_server_survives, run_cmd, uid


def _signup(c, u, password="P@ssw0rd"):
    return run_cmd(c, "sign_up", username=u, password=password, email=f"{u}@test.com")


def test_sign_in_wrong_password(lonely_server):
    c = lonely_server
    u = f"wp_{uid()}"
    _signup(c, u)
    r = run_cmd(c, "sign_in", username=u, password="WRONG_password")
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert "password" in r["responses"][0]["result"].lower()
    assert_server_survives(c)


def test_sign_in_nonexistent_user(lonely_server):
    c = lonely_server
    r = run_cmd(c, "sign_in", username=f"ghost_{uid()}", password="whatever")
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert "not exist" in r["responses"][0]["result"].lower()
    assert_server_survives(c)


def test_sign_up_duplicate_username(lonely_server):
    c = lonely_server
    u = f"dup_{uid()}"
    _signup(c, u)
    r = _signup(c, u)
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert "exist" in r["responses"][0]["result"].lower() or "duplicate" in r["responses"][0]["result"].lower()
    assert_server_survives(c)


def test_add_phone_user_duplicate_username(lonely_server):
    c = lonely_server
    u = f"dpu_{uid()}"
    number = f"0920{uid()}"
    run_cmd(c, "add_phone_user", username=u, phone_number=number, explanation="first")
    r = run_cmd(c, "add_phone_user", username=u, phone_number=f"0921{uid()}", explanation="second")
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_add_phone_number_duplicate_number(lonely_server):
    c = lonely_server
    u1, u2 = f"dn1_{uid()}", f"dn2_{uid()}"
    number = f"0922{uid()}"
    run_cmd(c, "add_phone_user", username=u1, phone_number=number, explanation="a")
    run_cmd(c, "add_phone_user", username=u2, phone_number=f"0923{uid()}", explanation="b")
    r = run_cmd(c, "add_phone_number", username=u2, phone_number=number)
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_get_phone_user_by_name_nonexistent(lonely_server):
    c = lonely_server
    r = run_cmd(c, "get_phone_user_by_name", username=f"ghost_{uid()}")
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert "not exist" in r["responses"][0]["result"].lower() or "not found" in r["responses"][0]["result"].lower()
    assert_server_survives(c)


def test_get_phone_user_by_number_nonexistent(lonely_server):
    c = lonely_server
    r = run_cmd(c, "get_phone_user_by_number", phone_number=f"0000{uid()}")
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_edit_phone_user_nonexistent(lonely_server):
    c = lonely_server
    r = run_cmd(c, "edit_phone_user", username=f"ghost_{uid()}", phone_number="123",
                new_username="x", new_phone_number="456")
    assert r["responses"] is not None, (
        f"expected a structured error result, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_edit_phone_user_partial_parameters(lonely_server):
    # spec: only one of the parameters may be sent and the rest omitted
    c = lonely_server
    u = f"pp_{uid()}"
    run_cmd(c, "add_phone_user", username=u, phone_number=f"0924{uid()}", explanation="x")
    payload = [{
        "command_name": "edit_phone_user",
        "parameters": {
            "username": u,
            "phone_number": f"0925{uid()}",  # does not exist, but key layout is the point
            "new_phone_number": f"0926{uid()}",
        },
    }]
    r = c.send(payload)
    assert r["responses"] is not None, (
        f"server cannot handle omitted optional parameters, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_add_phone_user_missing_parameter(lonely_server):
    c = lonely_server
    payload = [{
        "command_name": "add_phone_user",
        "parameters": {"username": f"mp_{uid()}"},  # phone_number missing
    }]
    r = c.send(payload)
    assert r["responses"] is not None, (
        f"expected a structured error result for missing parameters, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_unknown_command_name(lonely_server):
    c = lonely_server
    r = run_cmd(c, "completely_unknown_command", username="x")
    assert r["responses"] is not None, (
        f"expected a structured error result for unknown command, got: {r['error']!r}"
    )
    assert "unknown" in r["responses"][0]["result"].lower() or "not supported" in r["responses"][0]["result"].lower()
    assert_server_survives(c)


def test_malformed_payload_object_instead_of_list(lonely_server):
    c = lonely_server
    r = c.send({"command_name": "sign_up", "parameters": {"username": "x", "password": "y", "email": "z@z.z"}})
    assert r["responses"] is not None, (
        f"server cannot handle malformed payload, got: {r['error']!r}"
    )
    assert_server_survives(c)


def test_empty_command_list(lonely_server):
    c = lonely_server
    r = c.send([])
    assert r["responses"] == [], f"expected an empty list reply, got: {r}"
    assert_server_survives(c)
