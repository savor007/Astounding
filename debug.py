import sys
import cv2
import numpy as np
import dpkt
from multiprocessing import pool
import requests
import pprint
import PyQt5

def TablePrint(content):
    format_str= pprint.pformat(content, width=98)
    pprint.pprint("|"+format_str+"|",)
    pprint.pprint('_'*100)
    pass 


print(sys.stdout.name)
TablePrint('test')
import pip

# installed_packages = pip.get_installed_distributions()

print(PyQt5.__version__)