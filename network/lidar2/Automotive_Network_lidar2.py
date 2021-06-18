import socket
import time
import multiprocessing
import sys
from tkinter import *
from queue import Queue
#from ../TkWIndow.tkwindow import MY_GUI
#import sys
sys.path.append("/home/nio/Documents/projects/Astounding/")    
import TkWIndow.tkwindow



#output= sys.stdout.output()

network_lidar_queue=Queue()
network_radar_queue=Queue()


class UDP_Receiver:
    def __init__(self, name, ip, port, blocksize=1024, timeout=180, GUI=None):
        self.ip=ip
        self.name=name
        self.port=port
        self.blocksize=blocksize
        self._udp_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_socket.bind((self.ip, self.port))
        self._udp_socket.settimeout(timeout)
        self._received_packages_num=0
        self.gui=GUI
        #self._udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
        #print("socket.SO_SNDBUF:"+str(socket.SO_SNDBUF))
        #print("socket.SO_RCVBUF"+str(socket.SO_RCVBUF))



    @property
    def received_packages_num(self):
        return self._received_packages_num


    def ReceiveDigram(self, signal_type="", task_queue=None):
        self._received_packages_num=0
        start_time=time.clock_gettime(0)
        end_time= start_time
        while True:
            try:
                data, addr= self._udp_socket.recvfrom(self.blocksize)
            except TimeoutError as error:
                break
            except Exception as error:
                print(type(error))
                print(error)
                break
            else:
                if self._received_packages_num == 0:
                    start_time= time.clock_gettime(0)
                else:
                    end_time= time.clock_gettime(0)
                self._received_packages_num+=1
                indicated_str= "Data Length:{:6d}, Source IP:{}, Received Time:{}, Duration:{:.4f},seconds, Total Packets Number is {}".format(len(data), addr, time.ctime(), end_time-start_time, self._received_packages_num )
                print(indicated_str)
                if task_queue is not None:
                    task_queue.put_nowait(indicated_str)

                #print("Data Length:{:6d}, Source IP:{}, Received Time:{}, Duration:{:.4f},seconds, Total Packets Number is {}".format(len(data), addr, time.ctime(), end_time-start_time, i ))
                # if signal_type == 'lidar' and task_queue:
                #     task_queue.put_nowait(indicated_str)
                #     #self.gui.print_lidar_data("Data Length:{:6d}, Source IP:{}, Received Time:{}, Duration:{:.4f},seconds, Total Packets Number is {}".format(len(data), addr, time.ctime(), end_time-start_time, i ))      
                # else:
                #     task_queue.put_nowait(indicated_str)
                    

                    #self.gui.print_radar_data("Data Length:{:6d}, Source IP:{}, Received Time:{}, Duration:{:.4f},seconds, Total Packets Number is {}".format(len(data), addr, time.ctime(), end_time-start_time, i ))      



    
if __name__ == "__main__":
    
    

    # radar_udp_rec=UDP_Receiver("Radar Receiver", "169.254.115.15", 9002, 65000, timeout=180, GUI=None)
    velodyne_udp_rec=UDP_Receiver("Velodyne Lidar Receiver","169.254.115.15",9003,65100,timeout=180, GUI=None)
    # p1=multiprocessing.Process(target=radar_udp_rec.ReceiveDigram, args=(None,))
    # p2=multiprocessing.Process(target=velodyne_udp_rec.ReceiveDigram, args=(None,))
    # p1.start()
    # p2.start()
    velodyne_udp_rec.ReceiveDigram()
