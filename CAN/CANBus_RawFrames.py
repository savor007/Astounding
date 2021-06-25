import can
import time
import os
from datetime import datetime
from pprint import pprint


class CANBusRawFrame_Reader(object):
    def __init__(self, can_channel, bitrate, bustype='socketcan', message_to_read=-1):
        self.can_channel=can_channel
        self.bitrate=bitrate
        self.bustype=bustype
        self._message_to_read= message_to_read
        self._can_comm_verbose=True
        self._can_comm_timeout=10
        self._start_time=0
        self._end_time=0
        self._receive_number = 0

    @property
    def receive_starttime(self):
        return self._start_time


    @property
    def receive_frames(self):
        return self._receive_number


    @property
    def message_to_read(self):
        return self._message_to_read


    @property
    def duration(self):
        return self._end_time - self._start_time


    @message_to_read.setter
    def message_to_read(self, num):
        self._message_to_read=num


    @property
    def can_comm_verbose(self):
        return self._can_comm_verbose


    @can_comm_verbose.setter
    def verbose(self, part_attribute):
        self._can_comm_verbose= part_attribute


    @property
    def can_comm_timeout(self):
        return self._can_comm_timeout


    @can_comm_timeout.setter
    def can_comm_timeout(self, timeout):
        self._can_comm_timeout=timeout



    def Start_CANChannel_RawFrames_Receive(self):
        """
    can_channel='can0' or 'can1'
    """
        try:
            bus= can.interface.Bus(bustype=self.bustype, channel=self.can_channel, bitrate=self.bitrate, timeout=self._can_comm_timeout)
        except Exception as error:
            print(error)
            return None
        i=0
        
        ##for msg in bus:
        while True:
            try:
                msg=bus.recv(timeout=self._can_comm_timeout)
                if msg is None:
                    #self._end_time= time.clock_gettime(0)
                    break
                elif i == 0:
                    self._start_time=time.clock_gettime(0)
                elif i != 0:
                    self._can_comm_timeout=35

            except Exception as error:
                print(error)
                break
            if self._can_comm_verbose == False:
                print("Identifier:{:4d}, Timestamp: {}, DataLength: {:2d}, Raw_Frame_Data: {}, is_FD: {}, Message_Type: {}, Error_Frame: {}, Extended_id:{}, Error_State_Indicator:{}./n".format(
                            msg.arbitration_id, datetime.fromtimestamp(msg.timestamp), msg.dlc, msg.data, msg.is_fd, msg.id_type, msg.is_error_frame, msg.is_extended_id,msg.error_state_indicator
                        )
                    )
            else:
                print("Identifier:{:4d}, Timestamp: {}, DataLength: {:2d}, Raw_Frame_Data: {}, is_FD: {}.".format(
                            msg.arbitration_id, datetime.fromtimestamp(msg.timestamp), msg.dlc, msg.data, msg.is_fd
                        )
                    )
            i+=1
            self._end_time= time.clock_gettime(0)
            self._receive_number=i
            if i>self._message_to_read & self._message_to_read>0:
                break
        return None
    




if __name__ == "__main__":
    #can_receiver('can0', 500000, 100)
    can_receiver=CANBusRawFrame_Reader('can0', 500000)
    can_receiver.message_to_read=-1
    can_receiver.can_comm_timeout=130
    can_receiver.Start_CANChannel_RawFrames_Receive()
    #print(can_receiver.duration)
    can_receive_result="CAN Playback:first packet receive time:{}, logging duration time:{} seconds, total received frames:{}.".format(datetime.fromtimestamp(can_receiver.receive_starttime), can_receiver.duration, can_receiver.receive_frames)
    print(can_receive_result)
    can_filename="can_receive_log_{}.txt".format(datetime.now().strftime('%Y_%m_%d_%H%M%S'))
    can_filepath="/mnt/a055017a-3fac-4681-894f-bde3f20cf0c5/CAN_Receive_Logs"
    with open(os.path.join(can_filepath, can_filename),"wb+") as can_logging_file:
        can_logging_file.write(can_receive_result.encode('utf-8'))