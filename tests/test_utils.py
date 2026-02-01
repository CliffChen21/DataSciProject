"""Unit tests for utility helpers."""
from datetime import datetime

from backend.utils.helpers import format_datetime, safe_get, truncate_text, validate_json_keys


def test_format_datetime():
    dt = datetime(2026, 2, 1, 12, 0, 0)
    assert format_datetime(dt) == "2026-02-01 12:00:00"


def test_safe_get():
    data = {"a": {"b": {"c": 1}}}
    assert safe_get(data, "a", "b", "c") == 1
    assert safe_get(data, "a", "x", default=0) == 0


def test_truncate_text():
    text = "abcdefghijklmnopqrstuvwxyz"
    assert truncate_text(text, max_length=10) == "abcdefg..."
    assert truncate_text("short", max_length=10) == "short"


def test_validate_json_keys():
    ok, msg = validate_json_keys({"a": 1, "b": 2}, ["a", "b"])
    assert ok is True
    ok, msg = validate_json_keys({"a": 1}, ["a", "b"])
    assert ok is False
    assert "Missing required keys" in msg
