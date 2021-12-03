# 创建作业
# 通过调用api的方式来达到定制的效果

更多关于transcoder api的操作，可以参考：
https://www.infoq.cn/zones/google/cloud/article/JGojU0VXPmu3AkNKQZoY

官方文档：
https://cloud.google.com/transcoder/docs#docs

首先是transcoder api支持的格式：
![123](https://user-images.githubusercontent.com/51317683/141058529-38ab2aa7-bc68-4eca-9d31-24f04473c802.png)

修改以下配置信息，通过该python脚本会创建一个job
uri="gs://{bucket-name}/{subtitle-name}",     //字幕需加上格式：例如：gs://m3u8-transcoder-input/test.srt

project_id = '${project-id}'
location = '${project-location}'

input_uri = 'gs://${input-bucket-name}/${your-video-name}'          //视频需加上格式：例如：gs://m3u8-transcoder-input/test.mp4
output_uri = 'gs://${output-bucket-name}/${folder-name}/'          //记得在最后加 “/”   例如：gs://video-output/output/

结果如下：

![test](https://user-images.githubusercontent.com/51317683/141058654-194ad48d-53f1-4f62-96ba-0b3fafd9d4b4.png)

查看job状态：
curl -X GET \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
https://transcoder.googleapis.com/v1/projects/126254666108/locations/asia-east1/jobs/${job-id}

删除job：
curl -X DELETE \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
"https://transcoder.googleapis.com/v1/projects/126254666108/locations/asia-east1/jobs/${job-id}"

output bucket的情况（在输出桶里你能够看到vtt格式的字幕以及ts格式、m3u8格式的视频文件）：
![12341241](https://user-images.githubusercontent.com/51317683/141058884-50cb1b92-63c0-4015-9003-4ffda906b5ae.png)

打开master.m3u8即可访问视频输出后的结果：
![231412412412](https://user-images.githubusercontent.com/51317683/141058903-c226f392-05c2-4a7f-a8f6-0d40ffaa3670.png)

