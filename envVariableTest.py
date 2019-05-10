import sys
import pytest

#sys.argv[1] = Key
#sys.argv[2] = secret

def checker:
    if str(sys.argv[1]) == "[secure]":
        print("Not actually getting keys...")
        return false
    else:
        print("Environment variables are being received!!")
        return true


assert( checker() == True)
