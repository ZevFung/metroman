# coding=utf-8
"""
@author: ziWu
程序功能： 图片批量下载
"""
# 导入请求模块
import urllib.request
import os
import math
import re

opener = urllib.request.build_opener()

urlBase = "http://www.metroman.cn/image/rail/{0}"

global errList
errList = []


def requestImage(image, isAppendErr=True):
    try:
        imgUrl = urlBase.format(image)
        print("开始下载{0}".format(image))
        urllib.request.urlretrieve(imgUrl, './image/{0}'.format(image))
        print("结束下载{0},成功".format(image))
        if not isAppendErr:
            errList.remove(imgUrl)
            print('当前有{0}个请求失败'.format(len(errList)))
    except urllib.error.HTTPError:
        print("结束下载{0},失败".format(image))
        if isAppendErr:
            errList.append(imgUrl)
            print('当前有{0}个请求失败'.format(len(errList)))
    except urllib.error.URLError:
        print("结束下载{0},失败".format(image))
        if isAppendErr:
            errList.append(imgUrl)
            print('当前有{0}个请求失败'.format(len(errList)))
    print("----------------------------------------------------")


def getCount(number, index):
    length = number / math.pow(2, 13 - index)
    count = 0
    if (length - 257) < 258:
        count = 0
    else:
        count = (length - 257) / 258

    count = int(count) + 2
    return count


def downloadImage():
    # 遍历
    for a in range(8, 14):
        os.makedirs('./image/{}'.format(a), exist_ok=True)
        if a == 8:
            url = "{}/{}_{}.png".format(a, 0, 0)
            requestImage(url, True)
        else:
            x = getCount(7054, a)
            y = getCount(6952, a)
            for x1 in range(0, x):
                for y1 in range(0, y):
                    url = "{}/{}_{}.png".format(a, x1, y1)
                    requestImage(url, True)

    print("下载完毕")

    print('共有{0}个请求失败，请求地址如下：'.format(len(errList)))
    for item in errList:
        print(item)

    print('开始重新请求地址')
    while len(errList) > 0:
        for item in errList:
            image = re.findall(r"http://www.metroman.cn/image/rail/(.+)", item)
            if image and len(image) > 0:
                requestImage(image[0], False)
        print('当前还有{0}个请求失败'.format(len(errList)))
    print('结束重新请求地址')


if __name__ == '__main__':
    downloadImage()
