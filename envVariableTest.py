import sys
import os
import pytest

#print(os.environ['AWS_ACCESS_KEY_ID'])
# ^way to retrieve environment variables passed in from Travis CI repo settings!!


def checker():
    if str(sys.argv[1]) == "[secure]":
        print("Not actually getting keys...")
        return false
    else:
        print("Environment variables are being received!!")
        return true

assert( checker() == True)
