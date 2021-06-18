import grpc, datastream_pb2, datastream_pb2_grpc



def invoke_publish_msg(subcriber, msg_topic,msg_body):
    message= datastream_pb2.TopicData()
    message.topicName=msg_topic
    message.messageData=msg_body.encode()
    try:
        subcriber.PublishMessage(message)
        print("send message successfully")
    except Exception as error:
        print(error)



def SendMessage(message_topic="python_test_command",message_body=""):
    with grpc.insecure_channel('169.254.115.37:9889') as channel:
        Message_Dispatcher=datastream_pb2_grpc.DataStreamServiceStub(channel)
        invoke_publish_msg(Message_Dispatcher, message_topic, message_body)


if __name__ == "__main__":
    SendMessage("PEFCommand","Pause123")
    pass

