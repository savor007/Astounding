import datastream_pb2, datastream_pb2_grpc, grpc, time
from concurrent import futures
import random
from queue import Queue
import time



class gRPC_Server(datastream_pb2_grpc.DataStreamServiceServicer):
    def __init__(self):
        self.__token__=list()
        self.subscriber_mapping={"tokenholder":{},}
        self._terminate=dict()



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
        print(topic_data)
        while True:
            """
            will break when receiving a remove subscriber request
            """
            if self._terminate[token] == True:
                break
            time.sleep(2)
            yield datastream_pb2.TopicData(topicName="heart_beating", messageData="This is a stream service, so I have to keep the service yield message.".encode())
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
        print("received message. topic:{}, message body:{}".format(topic, msg))
        #if self.subscriber_mapping
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
        
        print(self.subscriber_mapping)
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


def gRPC_Server_func():
    xavier_rpc_server=gRPC_Server()
    server= grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    datastream_pb2_grpc.add_DataStreamServiceServicer_to_server(xavier_rpc_server, server)

    server.add_insecure_port('169.254.115.15:9889')
    server.start()
    print("gRPC Server Running")

    try:
        time.sleep(600)
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    gRPC_Server_func()
    pass