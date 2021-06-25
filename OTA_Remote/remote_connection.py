import boto3
import botocore
import time
import sys
sys.path.append("/home/nio/Documents/projects/Astounding/")    
from Configuration.Configuration import aws_connection, gRPC_Setting
# s3 = boto3.resource('s3')
class remote_control_server:
    def __init__(self, local_ip, remote_cloud_service=""):
        print("remote connection is connecting")
        self.local_ip = local_ip
        self.remote_cloud_service = remote_cloud_service

    def get_connection_config(self, selection=""):
        self.connection_config = ""

    def Get_Queue_url(self):
        """
        this function need overwrite
        :return:
        """
        raise NotImplementedError

    def Get_Queue_url(self):
        """
        this function will return a url for connection
        :return:
        """
        raise NotImplementedError

    def Enqueue_Element(self, service_token="", message=''):
        """

        :param message:
        :return:
        """
        raise NotImplementedError

    def Dequeue_Element(self, service_token="", delete=True, message_to_read=1):
        """

        :param message:
        :return:
        """
        raise NotImplementedError

    def Flush_Queue(self):
        """

        :return:
        """
        raise NotImplementedError


class AWS_Queue(remote_control_server):
    def __init__(self, local_ip_address, queue_name, remote_ip):
        super().__init__(local_ip=local_ip_address, remote_cloud_service=remote_ip)
        self.queue_name = queue_name
        self.url = None
        try:
            self.sqs = boto3.client('sqs')
        except Exception as error:
            print(type(error))

    def Get_Queue_url(self):
        try:
            # Get URL for SQS queue
            response = self.sqs.get_queue_url(QueueName=self.queue_name)
            print(response['QueueUrl'])
            self.url = response['QueueUrl']
        except botocore.exceptions.EndpointConnectionError as error:
            return None
        except botocore.exceptions.ClientError as error:
            response = self.sqs.create_queue(
                QueueName=self.queue_name,
                Attributes={
                    'DelaySeconds': '0',
                    'MessageRetentionPeriod': '86400'
                }
            )
            print(response['QueueUrl'])
            self.url = response['QueueUrl']

    def Enqueue_Element(self, service_token="incomplete", message=''):
        try:
            response = self.sqs.send_message(
                QueueUrl=self.url,
                MessageAttributes={
                    'service_token': {
                        'DataType': 'String',
                        'StringValue': service_token
                    },

                },
                MessageBody=(
                    message
                )
            )

            print(response['MessageId'])
        except Exception as error:
            print(error)
            return None
        return response['MessageId']

    def Dequeue_Element(self, service_token="incomplete", delete=True, message_to_read=1):
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=message_to_read,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=2
            )
        except Exception as error:
            print(error)
            return None
        messages = response.get('Messages')
        if messages is None:
            print("empty aws queue, no messages.")
            return None
        messages_result = list()
        for msg in messages:
            ReceiptHandle = msg.get('ReceiptHandle')
            msg_body = msg.get('Body')
            sent_time = msg.get('Attributes')['SentTimestamp']
            messages_attribute = msg.get('MessageAttributes')
            messages_result.append({"ReceiptHandle": ReceiptHandle, "message": msg_body, "sent_time": sent_time,
                                    "attributes": messages_attribute})
            if delete:
                # Delete received message from queue
                try:
                    self.sqs.delete_message(
                        QueueUrl=self.url,
                        ReceiptHandle=ReceiptHandle
                    )
                    #print('Received and deleted message: %s' % msg)
                except Exception as error:
                    print(error)
        print(len(messages_result))
        print(messages_result)
        return messages_result

    def Flush_Queue(self):
        try:
            self.sqs.purge_queue(QueueUrl=self.url)
        except Exception as error:
            print(error)


if __name__ == '__main__':
    sqs = AWS_Queue(local_ip_address= gRPC_Setting['local_service_ip'], remote_ip="aws sqs", queue_name=aws_connection["queue_name"])
    sqs.Get_Queue_url()
    sqs.Enqueue_Element(service_token="PEFCommand", message='Resume')
    result=None
#    result = sqs.Dequeue_Element(delete=True, message_to_read=1)
    if result is not None:
        for re in result:
            print(re['message'] + re['sent_time'])
    else:
        print("no element is aws sqs")
        # sqs.Flush_Queue()
    # sqs.Get_Queue_url()
    # sqs.Enqueue_Element_SQS('Resume')
    # sqs.Dequeue_Element_SQS(delete=False, message_to_read=6)
