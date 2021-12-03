# 转码作业的结果处理
# 通过pubsub为触发器创建Cloud Functions来对转码作业进行处理
以Pub/Sub作为触发器创建Cloud Functions，根据转码任务的完成消息，可以进行将输出文件移动到发布路径，并更新媒体资源系统或内容数据库。如果消息队列中收到的是转码失败消息，则做相应的错误处理和通知，将源视频文件移动到单独的目录。
# Functions相关配置
自定义Functions名字，并选择pubsub作为触发器，选择的topic为job里配置的topic
![functions-1](https://user-images.githubusercontent.com/51317683/143563046-d3f34673-9180-4eef-aa55-a2586105df2d.png)

在超时设置内，设置到最大540，按照默认的60s，执行未完成就就会报错time out
设置环境变量
![functions-2](https://user-images.githubusercontent.com/51317683/143563057-afb193fb-b373-46c0-9e43-f51a5626617a.png)
