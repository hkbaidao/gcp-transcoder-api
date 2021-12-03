#此为视频，字幕，音频的任务
#由于python库并不完善，只能通过curl来调用API创建任务
import os
import subprocess


def start():


    token_command = "gcloud auth application-default print-access-token"
    ret, val = subprocess.getstatusoutput(token_command)
    PROJECT_ID = "orange-309504"
    location = "asia-east1"

    input_uri = "\"gs://test-bucket-input/44_1_001.mkv\""
    output_uri = "\"gs://test-bucket-output/test-44-test/\""
    input_srt = "\"gs://test-bucket-input/44_1_001.srt\""

    track = "1"

    command = "curl -X POST \"https://transcoder.googleapis.com/v1/projects/" + PROJECT_ID + "/locations/" + location + "/jobs\" " + \
               "-H \"Authorization: Bearer \"" + val + \
               " -H \"Content-Type: application/json; charset=utf-8\"" + \
               " -d" + \
               " \'{ \"config\": { \"inputs\": [ { \"key\": \"input0\", \"uri\":" + input_uri + "}, { \"key\": \"caption_input0\", \"uri\":" + input_srt + "} ], \"editList\": [ { \"key\": \"atom1\", \"inputs\": [ \"input0\", \"caption_input0\" ] } ], \"elementaryStreams\": [ { \"key\": \"video-stream0\", \"videoStream\": { \"h264\":{ \"heightPixels\": 360, \"widthPixels\": 640, \"bitrateBps\": 550000, \"frameRate\": 60 } }}, { \"key\": \"audio-stream0\", \"audioStream\": { \"codec\": \"aac\", \"bitrateBps\": 64000, \"channelCount\": 2, \"mapping\": [ { \"atomKey\": \"atom1\", \"inputKey\": \"input0\", \"inputTrack\": 1, \"inputChannel\": 0, \"outputChannel\": 0 },{ \"atomKey\": \"atom1\", \"inputKey\": \"input0\", \"inputTrack\": 1, \"inputChannel\": 1, \"outputChannel\": 1} ]} }, { \"key\": \"text-stream0\", \"textStream\": { \"codec\": \"webvtt\", \"languageCode\": \"en-US\", \"mapping\": [ {\"atomKey\": \"atom1\", \"inputKey\": \"caption_input0\", \"inputTrack\": 0 } ] }  } ], \"muxStreams\": [ { \"key\": \"sd\", \"container\": \"ts\", \"elementaryStreams\": [ \"video-stream0\", \"audio-stream0\" ], \"segmentSettings\": { \"segmentDuration\": \"6s\", \"individualSegments\": true } }, { \"key\": \"subtitle\", \"container\": \"vtt\", \"elementaryStreams\": [ \"text-stream0\" ], \"segmentSettings\": { \"segmentDuration\": \"6s\", \"individualSegments\": true } } ], \"manifests\": [ { \"fileName\": \"master.m3u8\", \"type\": \"HLS\", \"muxStreams\": [ \"sd\", \"subtitle\" ] } ], \"output\": { \"uri\": " + output_uri + "}, \"pubsub_destination\": { \"topic\": \"projects/jianquan-test/topics/test-transcoder\"} } }\'"

    print("    " + command)

    data = os.system(command)
    print(data)



if __name__ == '__main__':
    start()
