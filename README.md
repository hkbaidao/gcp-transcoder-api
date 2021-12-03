# transcoder api solution proposal
# 架构说明
![subtitles solution proposal](https://user-images.githubusercontent.com/51317683/143562283-095ea4b3-7685-4783-862e-c8f8b473ccd2.jpg)

1. 通过ffmpeg视频编辑工具将软字幕从视频文件内剥离分成字幕文件以及视频文件
2. 以Cloud Storage作为触发器创建Cloud Functions，将字幕文件上传至Cloud Storage触发Cloud Functions进行自动化处理字幕格式的操作，以符合Transcoder API的要求
3. 以Cloud Storage作为触发器创建Cloud Functions，将视频文件上传至Cloud Storage触发Cloud Functions进行自动化转码的操作，在这里我们可以自定义对视频的操作，例如定制音轨输出，定制视频格式，视频清晰度调整等等，该Functions同时也会自动读取在另一个桶内的字幕文件，将字幕从分离出来的软字幕转化为支持在线的WebVTT格式的外挂字幕
4. 以Pub/Sub作为触发器创建Cloud Functions，根据转码任务的完成消息，可以进行将输出文件移动到发布路径，并更新媒体资源系统或内容数据库。如果消息队列中收到的是转码失败消息，则做相应的错误处理和通知，将源视频文件移动到单独的目录。
