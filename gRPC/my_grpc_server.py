import datastream_pb2, datastream_pb2_grpc, grpc, time
from concurrent import futures
import random
from queue import Queue
import time



class gRPC_Server(datastream_pb2_grpc.DataStreamServiceServicer):
    def __init__(self):
        self.__token__=list()
        self.subscriber_mapping=dict()



    def AddSubscriber(self, request, context):
        #AddSubscriber
        self.__token__.append(random.randint(2086083600,2147483640))
        print("this is a request from AddSubscriber")
        return datastream_pb2.SubscriberToken(subscriberToken=self.__token__[0])
        pass


    def RemoveSubscriber(self, request, context):
        print("remove a subscriber"+str(request.subscriberToken))
        del self.subscriber_mapping[request.subscriberToken]
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


    def SubscribeTopic(self, request, context):
        #print(request)
        token=request.subscriberToken.subscriberToken
        topic=request.topicName
    
        self.subscriber_mapping[token]={topic:['test','Resume', 'Pause']} 
        print(self.subscriber_mapping)
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


    def UnsubscribeTopic(self, request, context):
        pass


    def StartReadingTopicMessages(self, request, context):
        print("received request from StartReadingTopicMessage")
        token=request.subscriberToken
        topic_data=self.subscriber_mapping[token]
        print(topic_data)
        for topic, messages in topic_data.items():
            for message in messages:
                print("gRPC server send a message. topic:{}, message:{}.".format(topic, message))
                time.sleep(0.18)
                yield datastream_pb2.TopicData(topicName=topic, messageData=message.encode())
                #topic_data= datastream_pb2.TopicData()
                # if self.message_queue.empty() == False:
                #     message_send="free_run"
                # else:
                #     message_send=self.message_queue.get_nowait()
                #     self.message_queue.task_done()
                # yield datastream_pb2.TopicData(topicName=topic, messageData=message_send.encode())


    def StopReadingTopicMessages(self, request, context):
        # return datastream_pb2.TopicData(topicName=, messageData=)
        print("get a stopreading request.")
        return datastream_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        pass


    def ReadLatestTopicMessage(self, request, context):
        pass


    def GetAllSubscribedTopics(self, request, context):
        pass


    def GetSubscribedTopics(self, request, context):
        pass


    def PublishMessage(self, request, context):
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
    pass