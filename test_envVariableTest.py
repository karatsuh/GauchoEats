import sys
import os
import pytest

#print(os.environ['AWS_ACCESS_KEY_ID'])
# ^way to retrieve environment variables passed in from Travis CI repo settings!!


def checker():
    if str(os.environ['AWS_ACCESS_KEY_ID']) == "[secure]":
        print("Not actually getting keys...")
        return False
    else:
        print("\nEnvironment variables are being received!!")
        return True

def test_envTest():
    assert( checker() == True )
