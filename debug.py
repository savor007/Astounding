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
import netifaces
import json
import glob
from datetime import datetime

import progressbar
import os
can_filename="can_receive_log_{}.txt".format(datetime.utcnow().strftime('%Y_%m_%d_%H%M%S'))
can_filepath="/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/CAN_Receive_Logs"
with open(os.path.join(can_filepath, can_filename),"wb+") as can_logging_file:
        can_logging_file.write("test".encode('utf-8'))
list_of_can_logs= glob.glob("/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/CAN_Receive_Logs/*")
print(list_of_can_logs)
# widgets=[
#     ' [', progressbar.Timer(), '] ',
#     progressbar.Bar(),
#     ' (', progressbar.ETA(), ') ',
# ]
# for i in progressbar.progressbar(range(20), widgets=widgets):
#     time.sleep(0.1)

# import sys
# sys.path.append("/home/nio/Documents/projects/Astounding/") 
# sys.path.append("/home/nio/Documents/projects/Astounding/gRPC_comm") 
# from gRPC_comm import gRPC_PEF_PubishCommand, datastream_pb2, datastream_pb2_grpc

# ecu_ip_address= netifaces.ifaddresses('eth0').get(2)[0].get('addr')
# gRPC_PEF_PubishCommand.SendMessage("ECUStatus",json.dumps({"ECU_Address":ecu_ip_address, "ECU_Status":"ready"}))

print("lidar2 packets number is {}. The duration is:{:.2f} seconds.".format(12, 0.1224555))


# def TablePrint(content):
#     format_str= pprint.pformat(content, width=98)
#     pprint.pprint("|"+format_str+"|",)
#     pprint.pprint('_'*100)
#     pass 


# #print(sys.stdout.name)
# #TablePrint('test')

# # installed_packages = pip.get_installed_distributions()

# #print(PyQt5.__version__)
# # try:
# #     redis_op=redis.StrictRedis(host='10.144.130.30', port=6379,db=0)
# #     result=redis_op.setex(name='test1',time=60, value="NIIES_APAC_trans")
# #     result=redis_op.get('test1')
# #     print(result.decode('utf-8'))
# # except Exception as error:
# #     print(error)


# # try:
# #     s3=boto3.resource('s3',aws_access_key_id='AKIASW7332IZ4M4GPJXC', aws_secret_access_key='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')
# #     bucket=s3.Bucket('niiestrans')
# # except Exception as error:
# #     print(error)


# print("Identifier: {}".format(int("19a", 16)))

# t1=time.clock_gettime(0)
# time.sleep(2)
# print(time.clock_gettime(0)-t1)

# p = Popen(["gnome-terminal"])
# a=p.communicate("pwd", stdout=PIPE)
# print(a)
# #print("test",file=p)



