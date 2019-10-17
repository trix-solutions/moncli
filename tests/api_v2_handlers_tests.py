from nose.tools import *
import moncli

def setup():
    print('SETUP')


def teardown():
    print('TEARDOWN')


def test_basic():
    print('I RAN!', end='')