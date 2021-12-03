#此为无字幕的任务
import os
import subprocess


def start():


    token_command = "gcloud auth application-default print-access-token"
    ret, val = subprocess.getstatusoutput(token_command)
    PROJECT_ID = "project-id"
    location = "location"

    input_uri = "\"gs://bucket-name/object-name\""
    output_uri = "\"gs://bucket-name/folder-name/\""
    track = "1"

    command = "curl -X POST \"https://transcoder.googleapis.com/v1/projects/" +PROJECT_ID+ "/locations/" +location+ "/jobs\" " + \
              "-H \"Authorization: Bearer \"" + val + \
              " -H \"Content-Type: application/json; charset=utf-8\"" + \
              " -d" + \
              " \'{ \"config\": { \"inputs\": [ { \"key\": \"input0\", \"uri\":" +input_uri+"}], \"editList\": [ { \"key\": \"atom1\", \"inputs\": [ \"input0\", ] } ], \"elementaryStreams\": [ { \"key\": \"video-stream0\", \"videoStream\": { \"h264\":{ \"heightPixels\": 360, \"widthPixels\": 640, \"bitrateBps\": 55000, \"frameRate\": 60 }} }, { \"key\": \"audio-stream0\", \"audioStream\": { \"codec\": \"aac\", \"bitrateBps\": 64000, \"channelCount\": 2, \"mapping\": [ { \"atomKey\": \"atom1\", \"inputKey\": \"input0\", \"inputTrack\": "+track+", \"inputChannel\": 0, \"outputChannel\": 0 },{ \"atomKey\": \"atom1\", \"inputKey\": \"input0\", \"inputTrack\": "+track+", \"inputChannel\": 1, \"outputChannel\": 1} ]} } ], \"muxStreams\": [ { \"key\": \"sd\", \"container\": \"ts\", \"elementaryStreams\": [ \"video-stream0\", \"audio-stream0\" ], \"segmentSettings\": { \"segmentDuration\": \"6s\", \"individualSegments\": true } }, ], \"manifests\": [ { \"fileName\": \"master.m3u8\", \"type\": \"HLS\", \"muxStreams\": [ \"sd\", ] } ], \"output\": { \"uri\": " +output_uri+ "}, \"pubsub_destination\": { \"topic\": \"projects/project-id/topics/topic-name\"} } }\'"

    print("    " + command)

    data = os.system(command)
    print(data)



if __name__ == '__main__':
    start()
