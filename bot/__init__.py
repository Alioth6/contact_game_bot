from os import path

try:
    from nplus.settings.local import *
except ModuleNotFoundError:
    print(f'Please create local settings file')
