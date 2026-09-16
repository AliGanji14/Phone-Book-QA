import pytest

from conftest import run_cmd, uid


def test_sign_up_success(server):
    u = f"su_{uid()}"
    r = run_cmd(server, "sign_up", username=u, password="P@ssw0rd", email=f"{u}@test.com")
    assert r["error"] is None, f"unexpected error reply: {r['error']!r}"
    assert r["responses"][0]["command_name"] == "sign_up"
    assert "successfully" in r["responses"][0]["result"]


def test_sign_up_result_structure(server):
    u = f"st_{uid()}"
    r = run_cmd(server, "sign_up", username=u, password="P@ssw0rd", email=f"{u}@test.com")
    assert r["error"] is None
    item = r["responses"][0]
    assert set(item.keys()) == {"command_name", "result"}, f"unexpected response structure: {item}"


def test_sign_in_correct_password(server):
    u = f"si_{uid()}"
    run_cmd(server, "sign_up", username=u, password="P@ssw0rd", email=f"{u}@test.com")
    r = run_cmd(server, "sign_in", username=u, password="P@ssw0rd")
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "successfully" in r["responses"][0]["result"]


def test_logout_after_sign_in(server):
    u = f"lo_{uid()}"
    run_cmd(server, "sign_up", username=u, password="P@ssw0rd", email=f"{u}@test.com")
    run_cmd(server, "sign_in", username=u, password="P@ssw0rd")
    r = run_cmd(server, "logout", username=u)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "successfully" in r["responses"][0]["result"]


def test_logout_without_sign_in(server):
    # observation case: spec does not define it; server must not crash
    r = run_cmd(server, "logout", username=f"nobody_{uid()}")
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert server.alive()


def test_add_phone_user_with_explanation(server):
    u = f"pu_{uid()}"
    r = run_cmd(server, "add_phone_user", username=u, phone_number=f"0912{uid()}", explanation="friend")
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "successfully" in r["responses"][0]["result"]


def test_add_phone_user_without_explanation(server):
    # spec: explanation is optional
    u = f"po_{uid()}"
    r = run_cmd(server, "add_phone_user", username=u, phone_number=f"0913{uid()}")
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "successfully" in r["responses"][0]["result"]


def test_add_phone_number_to_existing_user(server):
    u = f"an_{uid()}"
    first = f"021{uid()}"
    second = f"026{uid()}"
    run_cmd(server, "add_phone_user", username=u, phone_number=first, explanation="work")
    r = run_cmd(server, "add_phone_number", username=u, phone_number=second)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "successful" in r["responses"][0]["result"]
    g = run_cmd(server, "get_phone_user_by_name", username=u)
    numbers = g["responses"][0]["result"]["phone_numbers"]
    assert first in numbers and second in numbers


def test_get_all_phone_users(server):
    u1, u2 = f"ga_{uid()}", f"gb_{uid()}"
    run_cmd(server, "add_phone_user", username=u1, phone_number=f"0914{uid()}", explanation="a")
    run_cmd(server, "add_phone_user", username=u2, phone_number=f"0915{uid()}", explanation="b")
    r = run_cmd(server, "get_all_phone_users")
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    result = r["responses"][0]["result"]
    names = [item["name"] for item in result]
    assert u1 in names and u2 in names


def test_get_phone_user_by_name_returns_explanation(server):
    u = f"ge_{uid()}"
    run_cmd(server, "add_phone_user", username=u, phone_number=f"0916{uid()}", explanation="colleague")
    r = run_cmd(server, "get_phone_user_by_name", username=u)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    result = r["responses"][0]["result"]
    assert result["name"] == u
    # spec: contact details include the explanation
    assert result.get("explanation") == "colleague", (
        f"explanation missing from contact details: {result}"
    )


def test_get_phone_user_by_number(server):
    u = f"gn_{uid()}"
    number = f"0917{uid()}"
    run_cmd(server, "add_phone_user", username=u, phone_number=number, explanation="home")
    r = run_cmd(server, "get_phone_user_by_number", phone_number=number)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    result = r["responses"][0]["result"]
    assert result["name"] == u
    assert number in result["phone_numbers"]
    # spec: contact details include the explanation
    assert result.get("explanation") == "home", (
        f"explanation missing from contact details: {result}"
    )


def test_edit_phone_user_username_only(server):
    u1, u2 = f"eu_{uid()}", f"ev_{uid()}"
    number = f"021{uid()}"
    run_cmd(server, "add_phone_user", username=u1, phone_number=number, explanation="x")
    r = run_cmd(server, "edit_phone_user", username=u1, phone_number=number,
                new_username=u2, new_phone_number=None)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    g = run_cmd(server, "get_phone_user_by_name", username=u2)
    assert g["responses"] is not None, f"renamed user not found: {g['error']!r}"
    assert number in g["responses"][0]["result"]["phone_numbers"]


def test_edit_phone_user_number_only(server):
    u = f"en_{uid()}"
    old_number, new_number = f"021{uid()}", f"028{uid()}"
    run_cmd(server, "add_phone_user", username=u, phone_number=old_number, explanation="x")
    r = run_cmd(server, "edit_phone_user", username=u, phone_number=old_number,
                new_username=None, new_phone_number=new_number)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    g = run_cmd(server, "get_phone_user_by_name", username=u)
    assert new_number in g["responses"][0]["result"]["phone_numbers"], (
        f"phone number was not updated: {g['responses'][0]['result']}"
    )


def test_remove_phone_user(server):
    u = f"rm_{uid()}"
    run_cmd(server, "add_phone_user", username=u, phone_number=f"0918{uid()}", explanation="x")
    r = run_cmd(server, "remove_phone_user", username=u)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "successfully" in r["responses"][0]["result"]
    all_users = run_cmd(server, "get_all_phone_users")["responses"][0]["result"]
    assert u not in [item["name"] for item in all_users], "removed user still listed"


def test_remove_phone_user_nonexistent(server):
    # spec: removing a non-existent contact must return an error, not success
    u = f"ghost_{uid()}"
    r = run_cmd(server, "remove_phone_user", username=u)
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    assert "not found" in r["responses"][0]["result"].lower() or "does not exist" in r["responses"][0]["result"].lower(), (
        f"removal of non-existent contact returned success: {r['responses'][0]['result']!r}"
    )


def test_phone_commands_require_authentication(server):
    # spec: phone book operations must run only after successful sign in
    u = f"anon_{uid()}"
    r = run_cmd(server, "add_phone_user", username=u, phone_number=f"0919{uid()}", explanation="x")
    assert r["responses"] is not None, f"unexpected error reply: {r['error']!r}"
    msg = r["responses"][0]["result"].lower()
    assert "sign in" in msg or "auth" in msg or "permission" in msg, (
        f"phone book command accepted without authentication: {r['responses'][0]['result']!r}"
    )
