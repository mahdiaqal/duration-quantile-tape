import ast
import hashlib
import json
import sys
from pathlib import Path
import pytest

BODY = "This test document recommends an initial timeout of one second."
HASH = hashlib.sha256(BODY.encode()).hexdigest()


def mocks(vm, kind="EXACT", lower=1000, upper=1000, status=200):
    vm.clear_mocks()
    vm.mock_web(r".*rfc[0-9]+.txt", {"status": status, "body": BODY})
    vm.mock_llm(r"(?s).*Extract the explicitly specified duration.*",
                json.dumps({"kind": kind, "lower_ms": lower, "upper_ms": upper}))


@pytest.fixture
def tape(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.warp("2026-10-05T00:00:00Z")
    mocks(direct_vm)
    contract = direct_deploy("contracts/DurationQuantileTape.py")
    contract.create_feed("rto", "Recommended initial timeout", 2)
    return contract


def test_acquired_interval(tape):
    tape.append("rto", "one", 6298, HASH)
    report = tape.get_report("rto", "one")
    assert report["text"] == BODY and report["hash"] == HASH
    assert report["state"] == "APPENDED" and report["lower_ms"] == 1000
    assert tape.quantile("rto", 50, 3600)["lower_ms"] == 1000


def test_ring_eviction_and_immutable_history(tape, direct_vm):
    tape.append("rto", "one", 1, HASH)
    mocks(direct_vm, lower=3000, upper=3000)
    tape.append("rto", "two", 2, HASH)
    mocks(direct_vm, "RANGE", 2000, 4000)
    tape.append("rto", "three", 3, HASH)
    assert [r["spec"]["sample"] for r in tape.window("rto")] == ["two", "three"]
    assert tape.get_report("rto", "one")["lower_ms"] == 1000
    assert tape.quantile("rto", 50, 3600)["lower_ms"] == 2000
    assert tape.quantile("rto", 100, 3600)["upper_ms"] == 4000
    assert tape.history(0, 20)[-1]["evicted_key"] == '["rto","one"]'


def test_unknown_does_not_change_window(tape, direct_vm):
    tape.append("rto", "one", 1, HASH)
    root = tape.get_feed("rto")["window_root"]
    mocks(direct_vm, "UNKNOWN", 0, 0)
    tape.append("rto", "unknown", 2606, HASH)
    assert tape.get_report("rto", "unknown")["state"] == "HELD"
    assert tape.get_feed("rto")["window_root"] == root


def test_hash_substitution(tape):
    tape.append("rto", "bad", 1, "f" * 64)
    assert tape.get_report("rto", "bad")["state"] == "HELD"
    assert tape.quantile("rto", 50, 3600)["state"] == "EMPTY"


def test_http_failure(tape, direct_vm):
    mocks(direct_vm, status=404)
    tape.append("rto", "missing", 1, HASH)
    assert tape.get_report("rto", "missing")["state"] == "HELD"


def test_replay(tape, direct_vm):
    tape.append("rto", "one", 1, HASH)
    with direct_vm.expect_revert("spent sample ID"):
        tape.append("rto", "one", 2, HASH)
    with direct_vm.expect_revert("already observed RFC"):
        tape.append("rto", "two", 1, HASH)


def test_principal(tape, direct_vm, direct_bob):
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("feed maintainer required"):
        tape.append("rto", "one", 1, HASH)
    assert tape.get_feed("rto")["accepted"] == 0


def test_cross_feed_binding(tape, direct_vm):
    tape.create_feed("other", "Recommended initial timeout", 2)
    tape.append("rto", "one", 1, HASH)
    with direct_vm.expect_revert("unknown sample in feed"):
        tape.get_report("other", "one")
    assert tape.window("other") == []
    tape.append("other", "one", 1, HASH)
    assert tape.get_report("other", "one")["spec"]["feed"] == "other"


def test_observation_freshness(tape, direct_vm):
    tape.append("rto", "one", 1, HASH)
    direct_vm.warp("2026-10-05T02:00:00Z")
    module = sys.modules[object.__getattribute__(tape, "_instance").__class__.__module__]
    module.gl.message_raw["datetime"] = "2026-10-05T02:00:00Z"
    assert tape.quantile("rto", 50, 3600)["state"] == "STALE"


def helpers():
    tree = ast.parse(Path("contracts/DurationQuantileTape.py").read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in ("canonical", "parse_interval", "reports_match", "rank_bounds")]
    scope = {"json": json}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "helpers", "exec"), scope)
    return scope


def test_strict_schema():
    parse = helpers()["parse_interval"]
    for value in [{"kind": "EXACT", "lower_ms": True, "upper_ms": 1},
                  {"kind": "UNKNOWN", "lower_ms": 1, "upper_ms": 1},
                  {"kind": "EXACT", "lower_ms": 1, "upper_ms": 2},
                  {"kind": "RANGE", "lower_ms": -1, "upper_ms": 2}]:
        assert parse(value) is None


def test_exact_equivalence():
    match = helpers()["reports_match"]
    report = {"kind": "EXACT", "lower_ms": 1000, "upper_ms": 1000, "state": "APPENDED"}
    assert match(report, dict(report))
    assert not match(report, {**report, "upper_ms": 1001})
    assert not match(report, {**report, "state": "HELD"})


def test_interval_rank_is_conservative():
    rank = helpers()["rank_bounds"]
    samples = [{"lower_ms": 1, "upper_ms": 9}, {"lower_ms": 3, "upper_ms": 4}]
    assert rank(samples, 50) == (1, 4)
    assert rank(samples, 100) == (3, 9)


def test_history_chain(tape):
    tape.append("rto", "one", 1, HASH)
    events = tape.history(0, 20)
    assert events[1]["previous"] == events[0]["root"]


def test_bounds(tape, direct_vm):
    with direct_vm.expect_revert("invalid quantity or capacity"):
        tape.create_feed("bad", "Recommended initial timeout", 1)
    with direct_vm.expect_revert("invalid quantile"):
        tape.quantile("rto", 101, 3600)
