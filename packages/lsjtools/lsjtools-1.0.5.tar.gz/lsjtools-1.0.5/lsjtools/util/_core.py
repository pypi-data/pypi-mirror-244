__all__ = ["makedirs"]

import os

def makedirs(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
