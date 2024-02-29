"""
Module provides tests to test the `epyt_flow.data.networks` module.
"""
import pytest
from epyt_flow.data.networks import load_anytown, load_hanoi, load_kentucky, load_ltown, \
    load_net1, load_net2, load_net3, load_net6, load_richmond, load_ctown, load_dtown, \
    load_balerma, load_bwsn1, load_bwsn2, load_micropolis, load_rural, load_ltown_a

from .utils import get_temp_folder


def test_net1():
    assert load_net1(get_temp_folder()) is not None


def test_net2():
    assert load_net2(get_temp_folder()) is not None


def test_net3():
    assert load_net3(get_temp_folder()) is not None


def test_net6():
    assert load_net6(get_temp_folder()) is not None


def test_anytown():
    assert load_anytown(get_temp_folder()) is not None


def test_ctown():
    assert load_ctown(get_temp_folder()) is not None


def test_dtown():
    assert load_dtown(get_temp_folder()) is not None


def test_richmond():
    assert load_richmond(get_temp_folder()) is not None


def test_balerma():
    assert load_balerma(get_temp_folder()) is not None


def test_micropolis():
    assert load_micropolis(get_temp_folder()) is not None


def test_bwsn1():
    assert load_bwsn1(get_temp_folder()) is not None


def test_bwsn2():
    assert load_bwsn2(get_temp_folder()) is not None


def test_rural():
    assert load_rural(get_temp_folder()) is not None


def test_kentucky():
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


def test_ltown_a():
    assert load_ltown_a(get_temp_folder()) is not None
