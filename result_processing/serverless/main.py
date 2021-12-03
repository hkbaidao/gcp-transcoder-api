from google.auth import compute_engine
from google.cloud import storage
import base64
import google.auth.transport.requests
import os
import requests
import json
import sys
import time

success_bucket = os.environ['SUCCESS_BUCKET']         #从cloud funtions中设置的环境变量里取值，该项为你要将任务成功的结果转移至的路径
failed_bucket = os.environ['FAILED_BUCKET']           #从cloud funtions中设置的环境变量里取值，该项为你要将任务失败的结果转移至的路径
storage_client = storage.Client()

def hello_pubsub(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')                      
    message = json.loads(pubsub_message)                                                    #将topic的消息转化为json格式
    job_name = message['job']['name']                                                       #提取消息里的job.name并赋值给job_name，该项为任务的名称 格式为 projects/project-id/locations/location-id/jobs/job-id
    job_status = message['job']['state']                                                    #提取消息里的job.state并赋值给job_status，该项为任务的状态 SUCCEEDED和FAILED
    
    cred = compute_engine.credentials.Credentials()                                         #获取token
    auth_req = google.auth.transport.requests.Request()
    cred.refresh(auth_req)
    
    api_url = "https://transcoder.googleapis.com/v1/" + job_name                            #api请求的格式

    headers = {
        "Authorization": "Bearer {}".format(cred.token),
    }
    
    response = requests.get(headers=headers, url=api_url)                                   #发起请求 curl GET请求
    text = response.text                                                                    #获取请求返回的结果
    jsonobj = json.loads(text)                                                              #将返回的结果转化为json格式
    output_path = jsonobj['config']['output']['uri'].split('/',3)                           #从json里取值，该项为job配置的输出路径，取出来的格式为 ['gs:', '', 'bucket-id', 'folder/folder/']
    input_path = jsonobj['config']['inputs'][0]['uri'].split('/',3)                         #从json里取值，该项为job配置的输出路径，取出来的格式为 ['gs:', '', 'bucket-id', 'folder/folder/object']

    if job_status == "SUCCEEDED":                                                           #判断，如果job状态为SUCCEEDED，执行以下复制操作，将成功结果转移到成功路径
        source_bucket = storage_client.bucket(output_path[2])                               #该项为源桶，取上方output_path的第三项，即bucket-id
        destination_bucket = storage_client.bucket(success_bucket)                          #该项为目的桶，取上方定义的success_bucket
        source_blobs = source_bucket.list_blobs(prefix=output_path[3])                      #该项为源对象，对源桶按文件夹的开头进行遍历，将其他不相关的文件夹过滤
        for source_blob in source_blobs:                                                    #遍历上方的源对象，对每一个源对象进行操作
            destination_blob = destination_bucket.blob(source_blob.name)                    #目的对象，不更改名字
            (token, bytes_rewritten, total_bytes) = destination_blob.rewrite(source_blob)   #将源对象copy至目的桶内
            time.sleep(0.3)                                                                 #每0.3秒进行一个copy操作，如不设置该项，则会报错，too many request，可以适当的调整该项的数字以适应项目的实际情况
            source_bucket.delete_blob(source_blob.name)                                     #将已复制的源对象从源桶内删除
            print(                                                                          #输出
                "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
                    source_blob.name,
                    source_bucket.name,
                    destination_blob.name,
                    destination_bucket.name,
                )
            )
    if job_status == "FAILED":                                                              #判断，如果job状态为FAILED，执行以下复制操作，将失败结果转移到失败路径
        source_bucket = storage_client.bucket(input_path[2])                                #该项为源桶，取上方input_path的第三项，即bucket-id
        source_blob = source_bucket.blob(input_path[3])                                     #该项为源对象，取上方input_path的第四项，即folder/folder/object
        destination_bucket = storage_client.bucket(failed_bucket)                           #该项为目的桶，取上方定义的failed_bucket
        destination_blob = destination_bucket.blob(source_blob.name)                        #目的对象，不更改名字
        
        (token, bytes_rewritten, total_bytes) = destination_blob.rewrite(source_blob)       #将源对象copy至目的桶内
        
        source_bucket.delete_blob(source_blob.name)                                         #将已复制的源对象从源桶内删除
        
        print(                                                                              #输出
            "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
                source_blob.name,
                source_bucket.name,
                destination_blob.name,
                destination_bucket.name,
            )
        )
