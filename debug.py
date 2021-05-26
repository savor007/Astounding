import sys
#import cv2
#import numpy as np
import dpkt
from multiprocessing import pool
import requests
import pprint
import PyQt5
import redis
import boto3, botocore
import time
from subprocess import Popen, PIPE



def TablePrint(content):
    format_str= pprint.pformat(content, width=98)
    pprint.pprint("|"+format_str+"|",)
    pprint.pprint('_'*100)
    pass 


#print(sys.stdout.name)
#TablePrint('test')

# installed_packages = pip.get_installed_distributions()

#print(PyQt5.__version__)
# try:
#     redis_op=redis.StrictRedis(host='10.144.130.30', port=6379,db=0)
#     result=redis_op.setex(name='test1',time=60, value="NIIES_APAC_trans")
#     result=redis_op.get('test1')
#     print(result.decode('utf-8'))
# except Exception as error:
#     print(error)


# try:
#     s3=boto3.resource('s3',aws_access_key_id='AKIASW7332IZ4M4GPJXC', aws_secret_access_key='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')
#     bucket=s3.Bucket('niiestrans')
# except Exception as error:
#     print(error)


print("Identifier: {}".format(int("19a", 16)))

t1=time.clock_gettime(0)
time.sleep(2)
print(time.clock_gettime(0)-t1)

p = Popen(["gnome-terminal"])
a=p.communicate("pwd", stdout=PIPE)
print(a)
#print("test",file=p)



