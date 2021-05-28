from tkinter import *
from TkWIndow.tkwindow import MY_GUI
import multiprocessing
from network.Automotive_Network import UDP_Receiver
from queue import Queue


radar_udp_rec=UDP_Receiver("Radar Receiver", "169.254.115.15", 9002, 65000, timeout=180, GUI=None)
velodyne_udp_rec=UDP_Receiver("Velodyne Lidar Receiver","169.254.115.15",9001,timeout=180, GUI=None)
init_window.after(500,__update)
p1=multiprocessing.Process(target=radar_udp_rec.ReceiveDigram, args=(None,))
p2=multiprocessing.Process(target=velodyne_udp_rec.ReceiveDigram, args=(None,))
p1.start()
p2.start()
