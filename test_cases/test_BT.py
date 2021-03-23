import pytest


@pytest.fixture(scope='function')
def open_BT():
    print("open BT")


def test_BT_onoff():
    BT = 'on'
    assert BT == 'on'


def test_BT_connect(open_BT, BT_name=123):
    assert BT_name == "hello"


if __name__ == '__main__':
    pytest.main(['-v -s', 'test_BT.py'])
