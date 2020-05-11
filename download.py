import json
import os
import time

import requests

class Downloader():
    def __init__(self):
        self.getHtmlHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }

        self.downloadVideoHeaders = {
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av26522634',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

    def getHtml(self, url):
        try:
            response = requests.get(url=url, headers=self.getHtmlHeaders)
            print(response.status_code)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            print('请求Html错误:')


    def getVlistUrlByUid(self, uid, ps):
        return 'https://api.bilibili.com/x/space/arc/search?mid=' + str(uid) + '&ps=100&tid=0&pn=1'

    def getVlistByUser(self, uid):
        try:
            apiUrl = self.getVlistUrlByUid(uid, 1)
            response = requests.get(url=apiUrl, headers=self.getHtmlHeaders)
            vlist = json.loads(response.content)['data']['list']['vlist']
            result = []
            if(vlist):
                for v in vlist:
                    result.append(v['bvid'])
            return result

        except requests.RequestException:
            print('failed to get video list for ' + str(uid))

    def downloadVideoByBvid(self, bvid):
        try:
            os.system('you-get -o d:/vedio/ https://www.bilibili.com/video/' + bvid)

        except Exception:
            print('failed to download: ' + bvid)



a = Downloader()

apiUrl = 'https://api.bilibili.com/x/space/arc/search?mid=444348914&ps=10&tid=0&pn=9'
vlistJson = a.getVlistByUser('444348914')

for v in vlistJson:
    a.downloadVideoByBvid(v)
    time.sleep(20)