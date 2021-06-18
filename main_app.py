#!/usr/bin/sudo /usr/bin/python3
import multiprocessing
#from network.Automotive_Network_radar import UDP_Receiver
from queue import Queue
from CAN.CANBus_RawFrames import CANBusRawFrame_Reader
import subprocess
import time
import dpkt


# radar_udp_rec=UDP_Receiver("Radar Receiver", "169.254.115.15", 9002, 65000, timeout=180, GUI=None)
# velodyne_udp_rec=UDP_Receiver("Velodyne Lidar Receiver","169.254.115.15",9001,timeout=180, GUI=None)
# can_receiver=CANBusRawFrame_Reader('can0', 500000)
# can_receiver.message_to_read=-1
# can_receiver.can_comm_timeout=100
# can_receiver.Start_CANChannel_RawFrames_Receive()
#     #print(can_receiver.duration)
# print("logging duration time:{} seconds, total received frames:{}.".format(can_receiver.duration, can_receiver.receive_frames))
# p1=multiprocessing.Process(target=radar_udp_rec.ReceiveDigram, args=(None,))
# p2=multiprocessing.Process(target=velodyne_udp_rec.ReceiveDigram, args=(None,))
# p3=multiprocessing.Process(target=can_receiver.Start_CANChannel_RawFrames_Receive)
# p1.start()
# p2.start()
# p3.start()
# print("logging duration time:{} seconds, total received frames:{}.".format(can_receiver.duration, can_receiver.receive_frames))
#subprocess.call(['python3','/home/nio/Documents/projects/Astounding/CAN/CANBus_RawFrames.py'])
subprocess.call(['gnome-terminal','--','python3', 'CANBus_RawFrames.py'],cwd='/home/nio/Documents/projects/Astounding/CAN/')
subprocess.call(['gnome-terminal','--','python3', 'Automotive_Network_lidar2.py'],cwd='/home/nio/Documents/projects/Astounding/network/lidar2/')
subprocess.call(['gnome-terminal','--','python3', 'Automotive_Network_radar.py'],cwd='/home/nio/Documents/projects/Astounding/network/radar/')
#p= subprocess.Popen(['tcpdump', 'udp', '-i', 'eth0', 'port', '9003', '-w', '/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/receivePCAP/lidar2.pcap'],shell=True, stdout=subprocess.PIPE, stderr= subprocess.STDOUT)
#p=subprocess.call(['gnome-terminal','--','tcpdump', 'udp -i eth0 port 9003 -w /home/nio/Documents/test1.pcap'],cwd='/home/nio/Documents/projects/Astounding/network/radar/')
#time.sleep
#p=subprocess.Popen('tcpdump udp -i eth0 port 9003 -w /home/nio/Documents/test1.pcap',stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#p.wait(10)
#p.kill()
commandsentence1='tcpdump udp -i eth0 port 9003 -w /home/nio/Documents/test1.pcap'.split()
commandsentence2='tcpdump udp -i eth0 port 9002 -w /home/nio/Documents/test2.pcap'.split()
cmd1=subprocess.Popen(['echo','welcome'], stdout=subprocess.PIPE)
cmd2=subprocess.Popen(['sudo', '-S']+ commandsentence1, stdin=cmd1.stdout, stdout=subprocess.PIPE)
cmd3=subprocess.Popen(['sudo', '-S']+ commandsentence2, stdin=cmd1.stdout, stdout=subprocess.PIPE)
time.sleep(380)
cmd3=subprocess.Popen(['sudo', '-S','killall','tcpdump'], stdin=cmd1.stdout, stdout=subprocess.PIPE)
# cmd2.send_signal(subprocess.signal.SIGTERM)
# #cmd3.send_signal(subprocess.signal.SIGTERM)
# cmd2.kill()
# cmd3.kill()
# print(cmd2.stdout.read().decode())
# print(cmd3.stdout.read().decode())
pcap_file1=open('/home/nio/Documents/test1.pcap', mode='rb')
pcap_handler1=dpkt.pcap.Reader(pcap_file1)
pcap1_result=[{"timestamp":timestamp, "packet":str_buffer, "length":len(str_buffer)} for timestamp, str_buffer in pcap_handler1]

print(len(pcap1_result))
print(pcap1_result[-1].get('timestamp')-pcap1_result[0].get('timestamp'))

