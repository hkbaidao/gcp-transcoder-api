from google.cloud import storage
from google.auth import compute_engine
import google.auth.transport.requests
import os

PROJECT_ID = os.environ['PROJECT_ID']                       #在环境配置中设置项目id
LOCATION = os.environ['LOCATION']                           #在环境配置中设置region
output_bucket = os.environ['OUTPUT_BUCKET']                 #在环境配置中设置视频输出的桶，切记不要将视频输入桶和输出桶设置为同一个，会导致cloud functions循环触发
srt_bucket = os.environ['SRT_BUCKET']                       #在环境配置中设置字幕的桶，切记不要将字幕的桶和输入的桶设置为同一个，会导致cloud functions重复触发
storage_client = storage.Client()

def hello_gcs(event, context):
    bucket_name = event['bucket']
    object_name = event['name']
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    input_name = object_name.split('.')

    input_uri = "gs://" + bucket_name + "/" + input_name[0] + ".mkv"            #源视频
    input_srt = "gs://" + srt_bucket + "/" + input_name[0] + ".srt"             #源字幕
    output_uri = "gs://" + output_bucket + "/" + input_name[0] +  "/"           #视频输出的桶，记得带 /
    
    cred = compute_engine.credentials.Credentials()                             #获取token进行身份验证

    auth_req = google.auth.transport.requests.Request()
    cred.refresh(auth_req)

    #以下是rest api方法，根据客户视频的需要对配置进行修改，当有视频文件上传至桶内，则cloud functions会自动创建任务并将视频进行切片，文字格式转换以及选择音轨的输出
    command = "curl -X POST \"https://transcoder.googleapis.com/v1/projects/" + PROJECT_ID + "/locations/" + location + "/jobs\" " + \
               "-H \"Authorization: Bearer \"" + cred.token + \
               " -H \"Content-Type: application/json; charset=utf-8\"" + \
               " -d" + \
               " \'{ \"config\": { \"inputs\": [ { \"key\": \"input0\", \"uri\":\"" + input_uri + "\"}, { \"key\": \"caption_input0\", \"uri\":\"" + input_srt + "\"} ], \"editList\": [ { \"key\": \"atom1\", \"inputs\": [ \"input0\", \"caption_input0\" ] } ], \"elementaryStreams\": [ { \"key\": \"video-stream0\", \"videoStream\": { \"h264\":{ \"heightPixels\": 360, \"widthPixels\": 640, \"bitrateBps\": 550000, \"frameRate\": 60 } }}, { \"key\": \"audio-stream0\", \"audioStream\": { \"codec\": \"aac\", \"bitrateBps\": 64000, \"channelCount\": 2, \"mapping\": [ { \"atomKey\": \"atom1\", \"inputKey\": \"input0\", \"inputTrack\": 1, \"inputChannel\": 0, \"outputChannel\": 0 },{ \"atomKey\": \"atom1\", \"inputKey\": \"input0\", \"inputTrack\": 1, \"inputChannel\": 1, \"outputChannel\": 1} ]} }, { \"key\": \"text-stream0\", \"textStream\": { \"codec\": \"webvtt\", \"languageCode\": \"en-US\", \"mapping\": [ {\"atomKey\": \"atom1\", \"inputKey\": \"caption_input0\", \"inputTrack\": 0 } ] }  } ], \"muxStreams\": [ { \"key\": \"sd\", \"container\": \"ts\", \"elementaryStreams\": [ \"video-stream0\", \"audio-stream0\" ], \"segmentSettings\": { \"segmentDuration\": \"6s\", \"individualSegments\": true } }, { \"key\": \"subtitle\", \"container\": \"vtt\", \"elementaryStreams\": [ \"text-stream0\" ], \"segmentSettings\": { \"segmentDuration\": \"6s\", \"individualSegments\": true } } ], \"manifests\": [ { \"fileName\": \"master.m3u8\", \"type\": \"HLS\", \"muxStreams\": [ \"sd\", \"subtitle\" ] } ], \"output\": { \"uri\": \"" + output_uri + "\"}, \"pubsub_destination\": { \"topic\": \"projects/project-id/topics/topic-name\"} } }\'"


    data = os.system(command)
    print(data)
