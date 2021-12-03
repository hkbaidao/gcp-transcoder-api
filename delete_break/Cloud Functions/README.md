# 也可以通过Cloud Functions部署一个自动化的字幕格式修改：

该Functions通过对上传字幕的逐行读取，并执行以上操作后，将输出的内容重新写回源文件内，即不用创建多一个桶来存放新字幕，也不会生成新文件，直接对源字幕进行修改：
以Cloud Storage作为触发器创建Cloud Functions，将字幕文件上传至Cloud Storage触发Cloud Functions进行自动化处理字幕格式的操作，以符合Transcoder API的要求

functions配置如下：

![141057622-22414d9c-163c-42c1-a4a6-d67ab8697ccc](https://user-images.githubusercontent.com/51317683/144533540-783d6740-e172-4478-a42b-8c3468041f30.png)
![2](https://user-images.githubusercontent.com/51317683/141057642-497adae6-2002-4274-9e17-a65907cf68bc.png)
![3](https://user-images.githubusercontent.com/51317683/141057649-7da2de3c-bec5-4719-acd1-8c6ca9bfdf7d.png)
