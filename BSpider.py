# B站爬虫
import requests
import re
import subprocess


class BilibliSpider(object):
    def __init__(self, av_num, save_path):
        self.save_path = save_path
        self.av_num = av_num
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }

    def get_index_html(self):
        '''
        获取请求页html
        :param av_num: int or str av号
        :return: str html文件
        '''
        av_num = str(self.av_num)
        url = "https://www.bilibili.com/video/{}".format(av_num)
        # 忽略证书验证
        content = requests.get(url, headers=self.headers, verify=False).content.decode()
        return content

    def get_true_addree(self, content):
        '''
        获取真实视频和音频地址
        :param content: str 请求页html
        :return: dict 视频和音频文件的url
        '''
        # 音频url
        url_sound = re.findall(r'.*?"id":30280,"baseUrl":"(.*?30280\.m4s.*?)"', content)
        # 视频url
        url_video = re.findall(r'.*?"baseUrl":.*"baseUrl":"(.*?30032\.m4s.*?)"', content)
        print(url_sound)
        print(url_video)
        url_dict = dict(url_sound=url_sound[0], url_video=url_video[0])
        return url_dict

    def download_source(self, url_dict):
        '''
        构造请求，下载视频文件和音频文件
        :param url_dict: dict 视频和音频文件的url
        :return:
        '''
        ref_url = "https://www.bilibili.com/video/{}".format(str(self.av_num))
        headers = {
            "Host": "cn-sdyt-cu-v-01.acgvideo.com",
            "Connection": "keep-alive",
            "Origin": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Accept": "*/*",
            "Referer": ref_url,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        try:
            video_source = requests.get(url_dict["url_video"], headers=headers, verify=False).content
            sound_source = requests.get(url_dict["url_sound"], headers=headers, verify=False).content
        except Exception as e:
            print(e)
        with open(self.save_path+self.av_num+".mp3", "wb") as f1:
            f1.write(sound_source)
        with open(self.save_path+self.av_num+".mp4", "wb") as f2:
            f2.write(video_source)
        print("下载完成")

    def video_convert(self):
        # 合并音频视频文件
        video_file = self.save_path+"\\%s.mp4" % self.av_num
        sound_file = self.save_path+"\\%s.mp3" % self.av_num
        dest_file = self.save_path+"\\%sc.mp4" % self.av_num
        cmd = "ffmpeg -i " + video_file + " -i " + sound_file + " -f mp4" + "  -loglevel fatal " + dest_file
        print(cmd)
        x = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("\t 正在合并视频，请稍后...")
        for log in x.stdout.readlines():
            print('[ffmpeg info] {0}'.format(log))
        for log in x.stderr.readlines():
            print('[ffmpeg error] {0}'.format(log))
        print('\t合并成功!\n {0}  and {1} -> {2}\n'.format(self.save_path + '\\%s.mp4' % self.av_num, self.save_path + '\\%s.mp3' % self.av_num,
                                                          self.save_path + '\\%sc.mp4' % self.av_num))
    def run(self):
        content = self.get_index_html()
        url_dict = self.get_true_addree(content)
        self.download_source(url_dict)
        self.video_convert()


def main():
    av_num = input("请输入av号：")
    save_path = input("请输入保存路径：")
    bs = BilibliSpider(av_num, save_path)
    bs.run()
