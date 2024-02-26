"""
Module provides tests to test the `epyt_flow.data.networks` module.
"""
import pytest
from epyt_flow.data.networks import load_anytown, load_hanoi, load_kentucky, load_ltown, \
    load_net1, load_net2, load_net3, load_richmond

from .utils import get_temp_folder


def test_net1():
    assert load_net1(get_temp_folder()) is not None


def test_net2():
    assert load_net2(get_temp_folder()) is not None


def test_net3():
    assert load_net3(get_temp_folder()) is not None


def test_anytown():
    assert load_anytown(get_temp_folder()) is not None


def test_richmond():
    assert load_richmond(get_temp_folder()) is not None


def test_kentuck():
    for i in range(1, 16):
        assert load_kentucky(wdn_id=i, download_dir=get_temp_folder()) is not None

    with pytest.raises(ValueError):
        load_kentucky(wdn_id=0, download_dir=get_temp_folder())

    with pytest.raises(ValueError):
        load_kentucky(wdn_id=16, download_dir=get_temp_folder())


def test_hanoi():
    assert load_hanoi(get_temp_folder()) is not None


def test_ltown():
    assert load_ltown(get_temp_folder()) is not None
