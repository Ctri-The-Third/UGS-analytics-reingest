import pytest
import logging

from re_ingest import *
from re_ingest import _inflate_json


def test_init():
    Ingestor("test", "test")
    Ingestor("test")


def test_inflate_correct_keys():
    keys = [
        "eventTimestamp",
        "eventVersion",
        "userID",
        "sessionID",
        "eventName",
        "eventUUID",
    ]

    for key in keys:
        desired_result = {key: 50, "eventParams": {}}
        actual_result = _inflate_json({key: 50})
        assert actual_result == desired_result


def test_inflate_incorrect_keys():

    key = "customParameter"
    desired_result = {"eventParams": {key: 50}}
    actual_result = _inflate_json({key: 50})
    assert actual_result == desired_result
