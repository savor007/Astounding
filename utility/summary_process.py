import redis
import boto3
import datetime
import json
from botocore.exceptions import ClientError
import os


class Playback_Summary_Uploader:
    def __init__(self, redis_host='127.0.0.1', redis_port= 6379,exist_duration=360000, sel_db=1, s3_bucket="", s3_key="",
                 enable_redis=True, enable_s3=True, bucketname="niiestrans",local_path="/home/sunwei/Documents/logs"):
        self.enable_redis= enable_redis
        self.enable_s3=enable_s3
        self.valid_duration= exist_duration
        self.base_log_folder= local_path
        if enable_redis:
            self.redis_repo=redis.Redis(host=redis_host, port= redis_port, db=sel_db)
        if enable_s3:
            self.my_s3=boto3.client('s3')
            self.bucketname= bucketname



    def upload_summary(self, result_string, tag_name="IES_Simulation", objectname="", filename=""):
        #+datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        if result_string =="":
            return None
        local_path= os.path.join(self.base_log_folder, filename)
        with open(local_path,"wb+") as logfile:
            logfile.write(result_string.encode('utf-8'))
        if self.enable_redis:
            self.redis_repo.lpush(tag_name,json.dumps({objectname:result_string}))
            self.redis_repo.expire(tag_name, self.valid_duration)
        if self.enable_s3:
            object_name=""
            if objectname == "":
                object_name= filename
            else:
                object_name=objectname
            try:
                response = self.my_s3.upload_file(local_path, self.bucketname,object_name)
            except ClientError as e:
                print(e)

    def read_all_summary_from_redis(self, tagname="IES_Simulation"):
        list_count=self.redis_repo.llen(tagname)
        for index in range(list_count):
            print(self.redis_repo.lindex(tagname, index))


if __name__ == '__main__':
    my_uploader=Playback_Summary_Uploader()
    my_uploader.upload_summary(json.dumps({"test":"test124"}),"simulate","2021-06-20_124511","2021-06-20_124511_playbacksummary.log")
    my_uploader.read_all_summary_from_redis("simulate")






