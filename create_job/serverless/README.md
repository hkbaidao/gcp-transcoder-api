# 以存储桶为触发器，创建cloud functions来自动触发任务（该函数需要设置三个桶）：
以Cloud Storage作为触发器创建Cloud Functions，将视频文件上传至Cloud Storage触发Cloud Functions进行自动化转码的操作，在这里我们可以自定义对视频的操作，例如定制音轨输出，定制视频格式，视频清晰度调整等等，该Functions同时也会自动读取在另一个桶内的字幕文件，将字幕从分离出来的软字幕转化为支持在线的WebVTT格式的外挂字幕

在cloud functions中设置环境变量：

![111](https://user-images.githubusercontent.com/51317683/141056407-ab78c155-5a7f-4164-a3a9-e614e0470f8f.png)
