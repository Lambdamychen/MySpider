# MySpider
## B站爬虫脚本 from Anosiga--A total new hand
* 测试时间：2019.4.7 
### 说明：该脚本只适用于带av号的视频，对于番剧是无力的，如果有前辈知道如何爬番剧，还请指导
### 技术概览：
        1.使用fiddler抓包发现，B站加载一个视频时，视频和音频分开加载，在网页源码中可以找到视频和音频加载的真实url
        2.使用requests分别下载视频和音频请求的真实url，使用ffmpeg合成视频音频即可，ffmpeg基本命令请参考:https://blog.csdn.net/kingvon_liwei/article/details/79271361
        3.使用PyInstaller将.py打包成.exe文件，依赖包见requirements.txt(不打包请跳过本条)
#### 留在最后：
        本人目前是一个初学者，所以代码不规范的地方还请包含
