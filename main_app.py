#!/usr/bin/sudo /usr/bin/python3
import multiprocessing, os
#from network.Automotive_Network_radar import UDP_Receiver
from queue import Queue
from CAN.CANBus_RawFrames import CANBusRawFrame_Reader
import subprocess
import time
import dpkt
import sys
sys.path.append("/home/nio/Documents/projects/Astounding/") 
sys.path.append("/home/nio/Documents/projects/Astounding/gRPC_comm") 
from gRPC_comm import gRPC_PEF_PubishCommand, datastream_pb2, datastream_pb2_grpc
import json
import netifaces
from datetime import datetime
import progressbar
import glob

widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]


if __name__ == "__main__":
    try:
        if os.environ.get('http_proxy'):
            del os.environ['http_proxy']
        if os.environ.get('https_proxy'):
            del os.environ['https_proxy']
        ecu_ip_address= netifaces.ifaddresses('eth0').get(2)[0].get('addr')
        gRPC_PEF_PubishCommand.SendMessage("ECUStatus",json.dumps({"ECU_Address":ecu_ip_address, "ECU_Status":"ready"}))
        can_receive_process=subprocess.call(['gnome-terminal','--','python3', 'CANBus_RawFrames.py'],cwd='/home/nio/Documents/projects/Astounding/CAN/')
        lidar2_receive_process=subprocess.call(['gnome-terminal','--','python3', 'Automotive_Network_lidar2.py'],cwd='/home/nio/Documents/projects/Astounding/network/lidar2/')
        radar_receive_process=subprocess.call(['gnome-terminal','--','python3', 'Automotive_Network_radar.py'],cwd='/home/nio/Documents/projects/Astounding/network/radar/')
        commandsentence1='tcpdump udp -i eth0 port 9003 -w /mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/receivePCAP/lidar2.pcap'.split()
        commandsentence2='tcpdump udp -i eth0 port 9002 -w /mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/receivePCAP/radar.pcap'.split()
        cmd1=subprocess.Popen(['echo','welcome'], stdout=subprocess.PIPE)
        cmd_receive_lidar2=subprocess.Popen(['sudo', '-S']+ commandsentence1, stdin=cmd1.stdout, stdout=subprocess.PIPE)
        cmd3_receive_radar=subprocess.Popen(['sudo', '-S']+ commandsentence2, stdin=cmd1.stdout, stdout=subprocess.PIPE)
        #gRPC_PEF_PubishCommand.SendMessage("ECUStatus",json.dumps({"ECU_Address":ecu_ip_address, "ECU_Status":"receiving"}))
        #time.sleep(380)
        for i in progressbar.progressbar(range(4200), widgets=widgets):
            time.sleep(0.1)
        cmd3=subprocess.Popen(['sudo', '-S','killall','tcpdump'], stdin=cmd1.stdout, stdout=subprocess.PIPE)
        """
        summary for the playback
        """
        playback_receive_report={"CAN":""}
        #####process the can log files############
        list_of_can_logs= glob.glob("/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/CAN_Receive_Logs/*")
        if len(list_of_can_logs) != 0:
            latest_can_log= max(list_of_can_logs, key=os.path.getctime)
            with open(latest_can_log,'rb+') as can_log:
                can_log_data= can_log.read().decode('utf-8')
            playback_receive_report["CAN"]=can_log_data
        ##########################################

        pcap_file1=open('/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/receivePCAP/lidar2.pcap', mode='rb')
        pcap_handler1=dpkt.pcap.Reader(pcap_file1)
        pcap1_result=[{"timestamp":timestamp, "packet":str_buffer, "length":len(str_buffer)} for timestamp, str_buffer in pcap_handler1]

        print("lidar2 packets number is {}. The duration is:{:.5f} seconds.".format(len(pcap1_result),pcap1_result[-1].get('timestamp')-pcap1_result[0].get('timestamp')))
        playback_receive_report["lidar2"]="lidar2 packets number is {}. The duration is:{:.5f} seconds.".format(len(pcap1_result),pcap1_result[-1].get('timestamp')-pcap1_result[0].get('timestamp'))
        ################################################################
        pcap_file2=open('/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/receivePCAP/radar.pcap', mode='rb')
        pcap_handler2=dpkt.pcap.Reader(pcap_file2)
        pcap2_result=[{"timestamp":timestamp, "packet":str_buffer, "length":len(str_buffer)} for timestamp, str_buffer in pcap_handler2]

        print("Radar packets number is {}. The duration is:{:.5f} seconds.".format(len(pcap2_result),pcap2_result[-1].get('timestamp')-pcap2_result[0].get('timestamp')))
        playback_receive_report["radar"]= "Radar packets number is {}. The duration is:{:.5f} seconds.".format(len(pcap2_result),pcap2_result[-1].get('timestamp')-pcap2_result[0].get('timestamp'))
        ##############################################
        syn_ts="Lidar2 first packet was received at {}. Radar first packet is received at {}. The synchonization error is {:.4f} milisecond".format(
            datetime.fromtimestamp(pcap1_result[0].get('timestamp')), 
            datetime.fromtimestamp(pcap2_result[0].get('timestamp')),
            1000*abs(pcap1_result[0].get('timestamp')-pcap2_result[0].get('timestamp'))
            )
        print(syn_ts)
        playback_receive_report["TimingSynchronization"]=syn_ts
        gRPC_PEF_PubishCommand.SendMessage("playbackreport",json.dumps(playback_receive_report))
        gRPC_PEF_PubishCommand.SendMessage("ECUStatus",json.dumps({"ECU_Address":ecu_ip_address, "ECU_Status":"idle"}))
    except Exception as error:
        print(error)
    