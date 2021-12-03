#此为无音轨编辑的任务
import json

from google.cloud.video import transcoder_v1
from google.cloud.video.transcoder_v1.services.transcoder_service import (
    TranscoderServiceClient,
)
from google.protobuf import duration_pb2 as duration


def create_job_with_periodic_images_spritesheet(project_id, location, input_uri, output_uri, srt_uri):

    client = TranscoderServiceClient()

    parent = f"projects/{project_id}/locations/{location}"
    job = transcoder_v1.types.Job()
    job.input_uri = input_uri
    job.output_uri = output_uri
    job.config = transcoder_v1.types.JobConfig(

        inputs=[
            transcoder_v1.types.Input(
                key="caption_input0",
                uri=srt_uri,
            ),
            transcoder_v1.types.Input(
                key="input0",
            )
        ],

        edit_list=[
            transcoder_v1.types.EditAtom(
                key="atom0",
                inputs=[
                    "caption_input0",
                    "input0",
                ],
            ),
        ],

        elementary_streams=[
            # This section defines the output video stream.
            transcoder_v1.types.ElementaryStream(
                key="video-stream0",
                video_stream=transcoder_v1.types.VideoStream(
                    h264=transcoder_v1.types.VideoStream.H264CodecSettings(
                    height_pixels=360,
                    width_pixels=640,
                    bitrate_bps=550000,
                    frame_rate=60,
                    ),
                ),
            ),
            # This section defines the output audio stream.
            transcoder_v1.types.ElementaryStream(
                key="audio-stream0",
                audio_stream=transcoder_v1.types.AudioStream(
                    codec="aac",
                    bitrate_bps=64000,
                ),
            ),
            # This section defines the output text stream.
            transcoder_v1.types.ElementaryStream(
                key="text-stream0",
                text_stream=transcoder_v1.types.TextStream(
                    codec="webvtt",
                ),
            ),
        ],
        # This section multiplexes the output audio and video together into a container.
        mux_streams=[
            transcoder_v1.types.MuxStream(
                key="sd",
                container="ts",
                elementary_streams=["video-stream0", "audio-stream0"],
                segment_settings=transcoder_v1.types.SegmentSettings(
                    segment_duration=duration.Duration(seconds=6),
                    individual_segments=True
                ),
            ),
            transcoder_v1.types.MuxStream(
                key="subtitle",
                container="vtt",
                elementary_streams=["text-stream0"],
                segment_settings=transcoder_v1.types.SegmentSettings(
                    segment_duration=duration.Duration(seconds=6),
                    individual_segments=True
                ),
            ),
        ],
        manifests=[
            transcoder_v1.types.Manifest(
                file_name="master.m3u8",
                type_="HLS",
                mux_streams=["sd", "subtitle"],
            )
        ],
    )
    response = client.create_job(parent=parent, job=job)
    return response


from queue import Queue

q = Queue(maxsize=0)

project_id='project-id'
location='location'

if __name__ == '__main__':

    input_uri='gs://bucket-name/object-name'   
    srt_uri='gs://bucket-name/subtitle-name'    
    output_uri='gs://bucket-name/folder-name/'                                    

    print(input_uri)
    print(output_uri)
    response = create_job_with_periodic_images_spritesheet(project_id, location, input_uri, output_uri, srt_uri)
    print(f"Job: {response.name}")
