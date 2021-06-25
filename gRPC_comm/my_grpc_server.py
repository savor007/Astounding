import datetime

import datastream_pb2, datastream_pb2_grpc, grpc, time
from concurrent import futures
import random
from queue import Queue
import time
import json
import sys
import pathlib
sys.path.append(pathlib.Path(__file__).parent.absolute().parent.absolute())

from OTA_Remote.remote_connection import remote_control_server, AWS_Queue
from Configuration.Configuration import aws_connection, gRPC_Setting
from utility.summary_process import Playback_Summary_Uploader


ECU_Status=list()
last_command_receivetime=0


class gRPC_Server(datastream_pb2_grpc.DataStreamServiceServicer):
    def __init__(self):
        self.__token__=list()
        self.subscriber_mapping={"tokenholder":{},}
        self._terminate=dict()
        self.result_uploader=Playback_Summary_Uploader(redis_host='169.254.115.37')



    def AddSubscriber(self, request, context):
        #AddSubscriber
        self.__token__.append(random.randint(2086083600,2147483640))
        print("this is a request from AddSubscriber")
        
        return datastream_pb2.SubscriberToken(subscriberToken=self.__token__[0])
        pass


    def RemoveSubscriber(self, request, context):
        print("remove a subscriber"+str(request.subscriberToken))
        self._terminate[request.subscriberToken]=True
        del self.subscriber_mapping[request.subscriberToken]
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


    def SubscribeTopic(self, request, context):
        #print(request)
        token=request.subscriberToken.subscriberToken
        topic=request.topicName
        self._terminate[token]=False
        #self.subscriber_mapping[token]={topic:['test','Resume', 'Pause']} 
        self.subscriber_mapping[token]=dict()
        print(self.subscriber_mapping)
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


    def UnsubscribeTopic(self, request, context):
        print("get a UnSubscriberdTopic request.")
        pass


    def StartReadingTopicMessages(self, request, context):
        print("received request from StartReadingTopicMessage")
        token=request.subscriberToken
        topic_data=self.subscriber_mapping[token]
        ECU_Busy = False
        try:
            if aws_connection['available']:
                sqs = AWS_Queue(local_ip_address= gRPC_Setting['local_service_ip'], remote_ip="aws sqs", queue_name=aws_connection["queue_name"])
                sqs.Get_Queue_url()
        except Exception as error:
            print(error)
 
        while True:
            """
            will break when receiving a remove subscriber request
            """
            if self._terminate[token] == True:
                break
            if aws_connection['available']:
                time.sleep(0.5)
            else:
                time.sleep(2)
            if len(ECU_Status) == 0:
                yield datastream_pb2.TopicData(topicName="Stream Service", messageData="have to keep the service by yielding message.No ECU connected".encode())
            else:
                yield datastream_pb2.TopicData(topicName="Stream Service", messageData=json.dumps(ECU_Status).encode())


            #####method1 send a command by pushlish grpc message, sent by subscriber##############
            topic_data=self.subscriber_mapping[token]
            for topic, messages in topic_data.items():
                for message in messages:
                    print("gRPC server send a message. topic:{}, message:{}.".format(topic, message))
                    yield datastream_pb2.TopicData(topicName=topic, messageData=message.encode())
                    time.sleep(0.5)
                ##############after send all of message, clear up the message list in that topic    
                self.subscriber_mapping[token][topic]=list()
            #####method2 check Messages in Redis[remote control pef resume/pause]######
            if aws_connection['available']:
                result = sqs.Dequeue_Element(delete=True, message_to_read=1)
                if result is None:
                    continue
                else:
                    aws_message_topic=result[0]['attributes']['service_token']['StringValue']
                    aws_message_body=result[0]['message']
                    yield datastream_pb2.TopicData(topicName=aws_message_topic, messageData=aws_message_body.encode())


            #####method3 Check Messages in AWS SQS[remote control pef resume/pause]#######


                #topic_data= datastream_pb2.TopicData()
                # if self.message_queue.empty() == False:
                #     message_send="free_run"
                # else:
                #     message_send=self.message_queue.get_nowait()
                #     self.message_queue.task_done()
                # yield datastream_pb2.TopicData(topicName=topic, messageData=message_send.encode())
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def StopReadingTopicMessages(self, request, context):
        # return datastream_pb2.TopicData(topicName=, messageData=)
        print("get a stopreading request.")
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


    def ReadLatestTopicMessage(self, request, context):
        print("get a ReadLatestTopic request.")
        pass


    def GetAllSubscribedTopics(self, request, context):
        print("get a GetAllSubscriberdTopic request.")
        pass


    def GetSubscribedTopics(self, request, context):
        print("get a GetSubscriberdTopic request.")
        pass


    def PublishMessage(self, request, context):
        print("get a PublishMessage request.")
        topic= request.topicName
        msg=request.messageData.decode()
        command_receivetime = time.time()
        if msg.lower() == "resume":
            command_receivetime= time.time()
        print("received message. topic:{}, message body:{}".format(topic, msg))
        #if self.subscriber_mapping
        if topic.lower() == "ecustatus":
            ECU_Status.append(json.loads(msg))
            return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        if topic.lower() == "playbackreport":
            ######Redis Server Available Upload Report to Redis#####
            date_str=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

            try:
                self.result_uploader.upload_summary(result_string=msg, tag_name="IES_Simulation",
                                                    objectname=date_str, filename="playback_summary_"+date_str+".log")
            except Exception as error:
                print(error)

        if topic.lower() == "pefcommand":
            for status in ECU_Status:
                if status.get("ECU_Status").lower() not in ("ready","idle"):
                    print("The ECU with IP address {} is not ready to receive playback data.Please check it again".format(status.get("ECU_Address")))
                    return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        global last_command_receivetime
        if command_receivetime - last_command_receivetime >=380:
            last_command_receivetime= command_receivetime
        else:
            return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        for commands in self.subscriber_mapping.values():
            #print(commands)
            try:
                message_list = commands.get(topic)
                if message_list is None or len(message_list) == 0:
                    commands[topic]=[msg]
                else:
                    message_list.append(msg)
                    commands[topic]=message_list
            except Exception as error:
                print(error)
        
        #print(self.subscriber_mapping)
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


def gRPC_Server_func():
    xavier_rpc_server=gRPC_Server()
    server= grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datastream_pb2_grpc.add_DataStreamServiceServicer_to_server(xavier_rpc_server, server)

    server.add_insecure_port('169.254.115.37:50051')
    server.start()
    print("gRPC Server Running")

    try:
        time.sleep(8000)
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    gRPC_Server_func()
    pass