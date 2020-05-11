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
            time.sleep(10)
            return requests.get(url=url, headers=self.getHtmlHeaders)
        except requests.RequestException:
            print('failed to get url: ' + url)

    def getVlistLengthByUid(self, uid):
        try:
            apiUrl = self.getVlistUrlByUid(uid, ps=20, pn=1)
            response = self.getHtml(apiUrl)
            count = json.loads(response.content)['data']['page']['count']
            print('getting vlist length for: ' + uid)
            print('count: ' + str(count))
            if count:
                return count
            else:
                return 0
        except Exception:
            print('failed to get vlist length for: '+uid)

    def getVlistUrlByUid(self, uid, pn, ps):
        return 'https://api.bilibili.com/x/space/arc/search?mid=' + uid + '&ps='+ str(ps) +'&tid=0&pn=' + str(pn)

    def getVlistByUser(self, uid):
        try:
            print('get vlist for: '+uid)
            videoCount = self.getVlistLengthByUid(uid)
            result = []
            pageSize = 20
            for i in range(0, videoCount//pageSize + 1):
                apiUrl = self.getVlistUrlByUid(uid, ps=pageSize, pn=i+1)
                response = self.getHtml(apiUrl)
                vlist = json.loads(response.content)['data']['list']['vlist']
                if vlist:
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