import time

import pytest
import requests

import services
from app import app
from config.settings import VERSION


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


@pytest.fixture
def github(monkeypatch):
    """Fake GitHub API: github.latest = tag to return, github.calls = number of requests"""
    class Github:
        latest = "v9.9.9"
        calls = 0
    state = Github()

    def fake_get(url, timeout=None):
        assert timeout is not None  # never wait forever
        state.calls += 1
        return FakeResponse({"tag_name": state.latest})

    monkeypatch.setattr(requests, "get", fake_get)
    return state


def test_parse_version():
    assert services.parse_version("v0.3.1") == (0, 3, 1)
    assert services.parse_version("0.4.0") == (0, 4, 0)
    assert services.parse_version("nightly") is None
    assert services.parse_version(None) is None


def test_compare_versions():
    assert services.compare_versions("v0.3.1", current="v0.3.1") is True
    assert services.compare_versions("v0.4.0", current="v0.3.1") is False
    assert services.compare_versions("v0.10.0", current="v0.9.0") is False  # not a string comparison
    assert services.compare_versions("v0.3.0", current="v0.3.1") is True  # dev ahead of the release
    assert services.compare_versions(None, current="v0.3.1") is True


@pytest.mark.parametrize("failure", [
    requests.exceptions.ConnectionError(),
    requests.exceptions.Timeout(),
    ValueError("not json"),
])
def test_get_newest_tag_returns_none_on_failure(monkeypatch, failure):
    def fake_get(url, timeout=None):
        if isinstance(failure, requests.exceptions.RequestException):
            raise failure
        return FakeResponse(failure)

    monkeypatch.setattr(requests, "get", fake_get)

    assert services.get_newest_tag() is None


def test_get_newest_tag_without_tag_name(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, timeout=None: FakeResponse({"message": "rate limit exceeded"}))

    assert services.get_newest_tag() is None


def test_popup_shows_both_versions_on_first_visit(github):
    page = app.test_client().get("/").get_data(as_text=True)

    assert "v9.9.9" in page
    assert github.calls == 1


def test_popup_still_shows_latest_version_when_cached(github):
    client = app.test_client()
    client.get("/")                      # first visit: GitHub is asked
    page = client.get("/").get_data(as_text=True)   # second visit: served from the cookie

    assert github.calls == 1             # no new request
    assert "v9.9.9" in page              # latest version is still the GitHub one, not the current one


def test_cache_expires_after_6_hours(github):
    client = app.test_client()
    client.set_cookie("last_update", str(time.time() - 7 * 3600))
    client.set_cookie("last_version", "v1.0.0")

    page = client.get("/").get_data(as_text=True)

    assert github.calls == 1
    assert "v9.9.9" in page


def test_no_popup_when_up_to_date(github):
    github.latest = VERSION

    page = app.test_client().get("/").get_data(as_text=True)

    assert "popup-latest" not in page


def test_failed_check_keeps_previous_version_and_does_not_retry_each_load(monkeypatch):
    calls = []

    def fake_get(url, timeout=None):
        calls.append(url)
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, "get", fake_get)
    client = app.test_client()
    client.set_cookie("last_update", str(time.time() - 7 * 3600))
    client.set_cookie("last_version", "v9.9.9")

    first = client.get("/").get_data(as_text=True)
    client.get("/")

    assert "v9.9.9" in first   # previous known version kept
    assert len(calls) == 1     # not retried on every page load
