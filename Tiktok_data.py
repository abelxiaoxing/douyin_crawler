import json
import os
import platform
import sys
import time
import traceback
import urllib
from urllib import parse
from urllib.parse import urlparse

import requests
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from retrying import retry
import re
import xlsxwriter
import xlwt
import requests
import re
import pandas as pd

class DouYin_Downloader():
    def __init__(self, url):
        self.url = url
        self.headers = {
                        'cookie': 'douyin.com; ttcid=be0e4c72ddac477998e093a240602ab719; ttwid=1%7CzCUAumsJLs5saY5D8bn7dI_X83RllITT15UpYe3ipo0%7C1637395882%7C364bf27783fe82923c5cccad2dac9c5ff32b3c291d30199c937c84eaab37b5d7; _tea_utm_cache_6383=undefined; MONITOR_WEB_ID=572de40d-1fff-4dc0-836b-44602750dc34; _tea_utm_cache_1300=undefined; passport_csrf_token_default=dd2988387b03b0773031755a2075362f; passport_csrf_token=dd2988387b03b0773031755a2075362f; n_mh=fxMGxUII0nrBEe6Ohr1FoUZfRGlBDBAaChEVJm8nhLw; sso_uid_tt=431643b7ae0a16e36948eaa4aa2fe0b8; sso_uid_tt_ss=431643b7ae0a16e36948eaa4aa2fe0b8; toutiao_sso_user=a6a32f4d3abd7f5cb1eb0d7eeabc84ae; toutiao_sso_user_ss=a6a32f4d3abd7f5cb1eb0d7eeabc84ae; odin_tt=c7d78d63f431f8c1e00e8485858263b58517378bcc76989d41f95a286edf145a24fcc6619fb54291391fe759ddb14183232da50c003e508cb62704e1655bf862; passport_auth_status_ss=411c4ce005860d1e47ae548b3d79891e%2C; sid_guard=170aabb93cd0ea3eaf455af0ebb02145%7C1637396118%7C5183999%7CWed%2C+19-Jan-2022+08%3A15%3A17+GMT; uid_tt=a079d0ed3a5f1cc20ac7df76ab3f771b; uid_tt_ss=a079d0ed3a5f1cc20ac7df76ab3f771b; sid_tt=170aabb93cd0ea3eaf455af0ebb02145; sessionid=170aabb93cd0ea3eaf455af0ebb02145; sessionid_ss=170aabb93cd0ea3eaf455af0ebb02145; sid_ucp_v1=1.0.0-KDM0ODMxYjI2MWZjZmEyOGQxODY1YTVjZTA1NmRmMGU4Y2I4ZGJkNGIKFwj-yaDfrPSnBxCW3eKMBhjvMTgGQPQHGgJobCIgMTcwYWFiYjkzY2QwZWEzZWFmNDU1YWYwZWJiMDIxNDU; ssid_ucp_v1=1.0.0-KDM0ODMxYjI2MWZjZmEyOGQxODY1YTVjZTA1NmRmMGU4Y2I4ZGJkNGIKFwj-yaDfrPSnBxCW3eKMBhjvMTgGQPQHGgJobCIgMTcwYWFiYjkzY2QwZWEzZWFmNDU1YWYwZWJiMDIxNDU; passport_auth_status=411c4ce005860d1e47ae548b3d79891e%2C; __ac_nonce=06199f5620065ae56f208; __ac_signature=_02B4Z6wo00f01zXQoHQAAIDDtdJaNVT9We819KTAAKz4E9gQs3vJPZfIoRD8mx-QJL-EU8pQPmUm00Hbx9IagiMBd-pmRH3pvT6ggFtdKm1nTnr9mNQ5kieWCKvz2tKcdqz4X0KRer6BBdFre3; douyin.com; s_v_web_id=verify_kw8xnlj5_8y3BLFlW_B5ca_45LT_8ppb_jfJU5qu9V9Fr; msToken=q3LpmVgozuLxZu1J26Ygd2uJ-NEm08J03SWFEp5p19c3kENTBcHPQ4Pci1G-3kUt8IvmnZI2QX7o9GE7Kfd8h92iHl5qTgfD_qOFqct2IikUtpSZA46xZWsAoA==; msToken=SdRjdYoFLEpaFsvHhGFNVA4c3TOj2BVyb0iO8GpzjS5n47A9Ziv5aNAbDI3uUqSkYWagXM1tIS4SakirPiSM0m-E9vwN1urTp6eM2MQ6wdZsb-MC_x5wig==; tt_scid=n.SR2EXQsnCoS52o0b6sEoX8j2W6Zjp8vEp8WuuaKfgHE6S5wBV4QKudldzcLitOae57',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
                        }
        self.text = requests.get(url=self.url, headers=self.headers).text

    def getTitle(self):
        return re.findall('<title data-react-helmet="true">(.*?)</title>', self.text)[0]

    def getVideoUrl(self):
        herf = re.findall('src(.*?)vr%3D%2', self.text)[1]
        video_url = requests.utils.unquote(herf).replace('":"', 'https:')
        return video_url

    def downloadVideo(self):
        title = self.getTitle()
        video_url = self.getVideoUrl()
        video_content = requests.get(url=video_url).content
        with open(title + '.mp4', mode='wb') as f:
            f.write(video_content)

    def getComment(self):
        decode_comment_url = requests.utils.unquote(self.text)
        comment = re.findall('"text":"(.*?)"', decode_comment_url)
        return comment

    def getLikeNum(self):
        likeNum = re.findall('<span class="CE7XkkTw">(.*?)</span>', self.text)[0]
        return likeNum

    def getCommentNum(self):
        commentNum = re.findall('<span class="CE7XkkTw">(.*?)</span>', self.text)[1]
        return commentNum

    def getCollectNum(self):
        collectNum = re.findall('<span class="CE7XkkTw">(.*?)</span>', self.text)[2]
        return collectNum

    def getRetransmission(self):
        retransmissionNum = re.findall('<span class="Uehud9DZ">(.*?)</span>', self.text)[0]
        return retransmissionNum

class VideoInit:
    # 初始化游标
    max_cursor = 0
    # 初始化视频数量
    video_count = 0
    # 成功爬取的视频数量
    success = 0
    # 失败爬取的视频数量
    error = 0

    # 初始化类型
    video = 0
    image = 0
    url = ''
    path = ''
    fileSize = 0
    downloaded = 0

    # 浏览器对象
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = None
    # driver = webdriver.Chrome(executable_path='Chrome/chromedriver.exe', desired_capabilities=caps)

    # 文件、图集文件夹命名变量
    authorName = 'none'
    desc = 'none'
    id = ''
    createTime = ''
    resolutionWidth = 1
    resolutionHeight = 1
    basename = 'none'
    ratio = 'none'
    dateTimeFormat = 'yyyyMMddHHmmss'
    descLength = 50
    videoName = '%authorName_%desc_%id'
    imageName = '%basename'
    imageAlbumName = '%authorName_%desc_%id'

    # 爬取配置
    userAvatarDownload = 0
    videoCoverDownload = 0
    videoMusicDownload = 0
    imageMusicDownload = 0
    quickDownload = 1

    # 全局请求头
    header = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="108", "Chromium";v="108", "Not=A?Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    # 初始化文件夹
    def __init__(self):
        # 判断文件夹是否存在
        if not os.path.exists('video'):
            os.mkdir('video')
        if not os.path.exists('video/主页'):
            os.mkdir('video/主页')
        if not os.path.exists('video/喜欢'):
            os.mkdir('video/喜欢')
        if not os.path.exists('video/合集'):
            os.mkdir('video/合集')
        if not os.path.exists('video/收藏'):
            os.mkdir('video/收藏')

        if os.path.exists('config.ini'):
            # 读取配置文件的命名规则
            cf = configparser.RawConfigParser()
            cf.read('config.ini', encoding='utf-8')
            self.dateTimeFormat = cf.get('NameRule', 'dateTimeFormat')
            self.descLength = int(cf.get('NameRule', 'descLength'))
            self.videoName = cf.get('NameRule', 'videoName')
            self.imageName = cf.get('NameRule', 'imageName')
            self.imageAlbumName = cf.get('NameRule', 'imageAlbumName')
            self.userAvatarDownload = int(cf.get('DownloadSettings', 'userAvatarDownload'))
            self.videoCoverDownload = int(cf.get('DownloadSettings', 'videoCoverDownload'))
            self.videoMusicDownload = int(cf.get('DownloadSettings', 'videoMusicDownload'))
            self.imageMusicDownload = int(cf.get('DownloadSettings', 'imageMusicDownload'))
            self.quickDownload = int(cf.get('DownloadSettings', 'quickDownload'))

        # 链接重定向
    def redirect(self, url):
        response = requests.get(url, headers=self.header)
        return response.url

    # 获取sec_uid
    @staticmethod
    def get_sec_uid(url):
        return url.split('user/')[1].split('?')[0]

    # 获取mix_id
    @staticmethod
    def get_mix_id(url):
        return url.split('detail/')[1].split('/')[0]

    # 获取用户信息
    def get_user_info(self, sec_uid):
        url = f'https://www.douyin.com/web/api/v2/user/info/?sec_uid={sec_uid}'
        response = requests.get(url, headers=self.header)
        return response.json()['user_info']['nickname']

    # 特殊字符处理
    @staticmethod
    def replace(title):
        title = title.replace('\\', '')
        title = title.replace('/', '')
        title = title.replace(':', '')
        title = title.replace('*', '')
        title = title.replace('?', '')
        title = title.replace('"', '')
        title = title.replace('<', '')
        title = title.replace('>', '')
        title = title.replace('|', '')
        title = title.replace(' ', '')
        title = title.replace('\n', '')
        return title

    # 验证是否为视频
    @staticmethod
    def is_video(data):
        try:
            if 'download_addr' in data['video'] or data.get('images', "") is None:
                return True
        except KeyError:
            return False

    # 结束输出
    def end(self):
        print('=====================================================')
        print('* 全部作品爬取完成')
        print(f'* 作品总数：{self.video_count}')
        print(f'* 成功爬取：{self.success}')
        print(f'* 失败爬取：{self.error}')
        print('=====================================================')
        # 数据重置
        self.max_cursor = 0
        self.video_count = 0
        self.success = 0
        self.error = 0
        self.video = 0
        self.image = 0
        self.url = ''
        self.path = ''
        self.driver.get('about:blank')


# 初始化浏览器
def GetWebdriver(ini):
    system_count=0
    system=platform.system()
    while system_count<3:
        try:
            if system == 'Windows':
                # windows
                ini.driver = webdriver.Chrome(executable_path='Chrome/chromedriver.exe', desired_capabilities=ini.caps)
                print('浏览器启动成功,当前系统为'+system+'系统')
                break
            elif system == 'Linux':
                # linux
                ini.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', desired_capabilities=ini.caps)
                print('浏览器启动成功,当前系统为'+system+'系统')
                break
            else:
                print(system+'系统不支持')
                exit()
            break
        except:
            system_count+=1
            print('浏览器启动失败，正在重试')
            time.sleep(1)


# 抓取cookies
def GetCookies(ini):
    print('*****************  正在更新cookie  *********************')
    header_add = ''
    for cookie_dict in ini.driver.get_cookies():
        header_add += cookie_dict['name'] + '=' + cookie_dict['value'] + ';' if cookie_dict['name'] != '' else \
            cookie_dict['value'] + ';'
    ini.header['cookie'] = header_add


# 抓取首页script[id="RENDER_DATA"]的数据
def GetFrontPageData(ini):
    print('*****************  正在处理首页数据，请勿操作  *********************')
    soup = BeautifulSoup(ini.driver.page_source, 'html.parser')
    response = soup.select('script[id="RENDER_DATA"]')[0].text
    response = urllib.parse.unquote(response)
    return json.loads(response)


# 获取浏览器里相应URL的数据包并解析爬取
def CrawlerByURL(ini, urlcontent,DouYinData):
    print('*****************   开始爬取作品数据，采集过程中浏览器不能最小化，可以不置顶  *********************')
    # 爬取后续加载的作品
    while True:
        logs_raw = ini.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        logs = [log for log in logs if (
                log["method"] == "Network.responseReceived" and urlcontent in log["params"]["response"]["url"])]
        print('获取到' + str(len(logs)) + '组数据，解析爬取中')

        for log in logs:
            try:
                request_id = log["params"]["requestId"]
                response = ini.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                data = response["body"]
                aweme_list = json.loads(data)
                # 获取是否有后续资源标记
                has_more = aweme_list['has_more']
                # 获取作品列表
                aweme_list = aweme_list['aweme_list']

                # !!!爬取作品集
                CrawlerAweme(ini, aweme_list,DouYinData)
                # 快速爬取
                if ini.quickDownload:
                    if ini.downloaded:
                        print('*****************  已爬取完最近更新视频，后续内容跳过  *********************')
                        ini.end()
                        return
                # 判断作品是否爬取完成
                if not has_more:
                    ini.end()
                    return
            except Exception as e:
                print(f'本组数据解析失败，自动跳过:{e}')
                continue
        print('新作品爬取完成，将继续滚动屏幕，加载作品，程序检测到新作品后会开始爬取')
        ini.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

# CrawlerAweme用来实现在
# ini 对象是该函数所需的一些配置信息，aweme_list 是一个视频列表，DouYinData 是一个二维列表，用于存储爬取的数据。
def CrawlerAweme(ini, aweme_list, DouYinData):
    # 遍历 aweme_list 中的每个视频，进行数据爬取和存储。
    for aweme in aweme_list:
        ini.video_count += 1
        title = 'None'

        # 将视频地址拼接为一个 URL，使用 DouYin_Downloader 对象下载该视频的 JSON 数据，然后从 JSON 数据中提取视频的标题、评论数、点赞数、转发数、收藏数等信息，并将这些信息以列表的形式添加到 DouYinData 中。
        video_url_ori= 'https://www.douyin.com/video/' + aweme["aweme_id"]
        DY = DouYin_Downloader(video_url_ori)
        title = DY.getTitle()
        comment = DY.getComment()
        likeNum = DY.getLikeNum()
        commentNum = DY.getCommentNum()
        collectNum = DY.getCollectNum()
        retransmissionNum = DY.getRetransmission()
        DouYinData.append([title, comment, likeNum, commentNum, collectNum, retransmissionNum, video_url_ori])

        try:
            # 从aweme中获取视频作者的昵称，保存在ini对象的authorName属性中。
            ini.authorName = aweme["author"]["nickname"]

            # 从aweme中获取视频的描述信息，调用ini对象的replace()方法将其中的占位符替换为实际的值，最终保存在ini对象的desc属性中。
            ini.desc = ini.replace(aweme["desc"])[:ini.descLength]

            # 从aweme中获取视频的ID，保存在ini对象的id属性中。
            ini.id = aweme["aweme_id"]

            # 从aweme中获取视频的创建时间，使用time模块将时间戳格式化为指定的日期时间格式，并保存在ini对象的createTime属性中。
            ini.createTime = time.strftime(ini.dateTimeFormat, time.localtime(aweme['create_time']))

            # 判断aweme是否为视频，is_video()是ini对象的一个方法，根据aweme的数据结构判断是否为视频。
            if ini.is_video(aweme):
                # 获取视频的长宽，存入ini
                ini.resolutionWidth = aweme['video']['width']
                ini.resolutionHeight = aweme['video']['height']
                # 获取视频的长宽比，存入ini
                ini.ratio = aweme['video']['ratio']
                print(f'正在爬取：【{ini.video_count}】' + title)

            # 如果aweme不是视频，则说明是图集。
            else:
                # 使用ini对象的replace()方法将ini.imageAlbumName中的占位符替换为实际的值，并将结果保存在imageAlbumTitle变量中。
                imageAlbumTitle = ini.replace(ini.imageAlbumName.replace('%authorName', ini.authorName).replace('%desc', ini.desc).replace('%id', ini.id).replace('%createTime', ini.createTime))

                print(f'正在爬取：【{ini.video_count}】' + imageAlbumTitle + '图集')
                # 创建路径所必要的文件夹
                if not os.path.exists(ini.path + '/' + imageAlbumTitle):
                    os.makedirs(ini.path + '/' + imageAlbumTitle)

            ini.success += 1
        except Exception as e:
            if ini.error < 6:
                log_name = ErrorLog(e)
                ini.error += 1
                print('爬取失败，自动跳过: ' + title)
                continue
            else:
                raise Exception('异常太多，终止爬取！')

        if ini.video_count%10==0:
            df = pd.DataFrame(DouYinData, columns=['Title', 'Comment', 'LikeNum', 'CommentNum', 'CollectNum', 'RetransmissionNum', 'VideoUrl'])
            df.to_excel('douyin_data.xlsx', index=False)


# 视频爬取
@retry(stop_max_attempt_number=3, wait_incrementing_start=5000, wait_incrementing_increment=10000)
def DownloadVideo(ini, video, title):
    fileSize = 0
    ini.downloaded = 0

    # 已经爬取的跳过
    if os.path.exists(f'{ini.path}/{title}.mp4'):
        print(f'{title} 文件已经存在，跳过')
        ini.downloaded = 1
        return fileSize
    # 请求视频
    response = requests.get(video, headers=ini.header)
    fileSize = len(response.content)
    # 写入视频
    with open(f'{ini.path}/{title}.mp4', 'wb') as f:
        f.write(response.content)
    response.close()
    return fileSize


# 图片和图片爬取
@retry(stop_max_attempt_number=3, wait_incrementing_start=5000, wait_incrementing_increment=10000)
def DownloadImageOrMusic(ini, image_url, imageAlbumTitle, title):
    fileSize = 0
    ini.downloaded = 0

    # 已经爬取的跳过
    if os.path.exists(f'{ini.path}/{imageAlbumTitle}/{title}'):
        print(f'{title} 文件已经存在，跳过')
        ini.downloaded = 1
        return fileSize
    # 请求文件
    print('正在爬取：' + title + '文件')
    response = requests.get(image_url, headers=ini.header)
    fileSize = len(response.content)
    # 写入文件
    with open(f'{ini.path}/{imageAlbumTitle}/{title}', 'wb') as f:
        f.write(response.content)
    response.close()
    return fileSize


# 写入日志
def ErrorLog(error):
    if not os.path.exists('video/Log'):
        os.mkdir('video/Log')
    # 获取当前时间
    log_name = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    errorContent = f'====================={date}=====================\n' \
                   f'{error}\n' \
                   f'=============================================================\n'
    # 写入错误日志
    with open(f'video/Log/{log_name}.log', 'a', encoding='utf-8') as f:
        f.write(errorContent)
    return log_name


# 程序主入口
def Start():
    try:
        ini = VideoInit()
        while True:
            print('=====================================================')
            print('*********** 抖音作品爬虫工具 V20230129.1 ***************')
            print('***************** \t作者：abelxiaoxing \t*********************')
            print('=====================================================')
            print('=====================================================')
            print('1.爬取用户主页作品(可用)\t\t2.爬取用户喜欢作品(可用)\n3.爬取用户作品合集(可用)\t\t4.爬取自己收藏作品(可用)\n5.批量爬取用户作品(可用)\t\t6.退出程序')
            print('=====================================================')
            choice = input('请输入序号选择类型：')
            if choice == '1':
                Home(ini)
            elif choice == '2':
                Like(ini)
            elif choice == '3':
                Collection(ini)
            elif choice == '4':
                Favorite(ini)
            elif choice == '5':
                MultipleDownload(ini)
            elif choice == '6':
                ini.driver.quit()
                sys.exit()
            else:
                print('输入错误，请重新输入！')
    except Exception as e:
        log_name = ErrorLog(e)
        log_name = ErrorLog(ini.url)
        log_name = ErrorLog(str(platform.platform()))
        log_name = ErrorLog(traceback.format_exc())
        input(f'程序出现错误，错误日志已保存至 video/Log 文件夹，联系作者请提交{log_name}.log文件！按任意键退出。')


# 爬取主页作品
def Home(ini, *url):
    column_num=0
    ini.url = url[0] if len(url) else input('请输入用户主页链接：')
    # 打开页面，通过人机认证
    print('*****************  请配合开展人机验证，然后等待数据读取及处理  *********************')
    GetWebdriver(ini)
    ini.driver.get(ini.url)
    WebDriverWait(ini.driver, 30).until(ec.title_contains('抖音'))
    time.sleep(5)
    # 获取cookies
    GetCookies(ini)
    # 处理首页数据
    data = GetFrontPageData(ini)
    # 数据节点的这个数字会变，所以直接查
    key = [a for a in data if 'uid' in data[a]][0]
    ini.authorName = ini.replace(data[key]["user"]["user"]["nickname"])
    # 创建文件夹
    ini.path = f'video/主页/{ini.authorName}'
    if not os.path.exists(ini.path):
        os.makedirs(ini.path)
    print('*****************  开始爬取首页视频，采集过程中浏览器不能最小化，可以不置顶  *********************')
    # 获取作品列表
    aweme_list = data[key]["post"]["data"]
    # 获取是否有后续资源标记
    hasMore = data[key]["post"]["hasMore"]
    # 爬虫数据list
    DouYinData = []
    # 读取作品
    for aweme in aweme_list:
        # 更新作品数量
        ini.video_count += 1
        column_num+=1
        # 作品标题
        title = 'None'
        # 初始化作品大小
        ini.fileSize = 0
        # 获取要爬取的数据存储到DouYinData
        video_url_ori= 'https://www.douyin.com/video/' + aweme["awemeId"]
        DY = DouYin_Downloader(video_url_ori)
        title = DY.getTitle()
        comment = DY.getComment()
        likeNum = DY.getLikeNum()
        commentNum = DY.getCommentNum()
        collectNum = DY.getCollectNum()
        retransmissionNum = DY.getRetransmission()
        DouYinData.append([title, comment, likeNum, commentNum, collectNum, retransmissionNum, video_url_ori])

        try:
            # 提取作品参数
            ini.desc = ini.replace(aweme["desc"])[:ini.descLength]
            ini.id = aweme["awemeId"]
            ini.createTime = time.strftime(ini.dateTimeFormat, time.localtime(aweme['createTime']))
            # 判断是视频还是图集
            if 'url' in aweme['download']:
                # 进一步提取视频参数
                ini.resolutionWidth = aweme['video']['width']
                ini.resolutionHeight = aweme['video']['height']
                ini.ratio = aweme['video']['ratio']
                print(f'正在爬取：【{ini.video_count}】' + title)
            else:
                imageAlbumTitle = ini.replace(ini.imageAlbumName.replace('%authorName', ini.authorName).replace(
                    '%desc', ini.desc).replace('%id', ini.id).replace('%createTime', ini.createTime))
                print(f'正在爬取：【{ini.video_count}】' + imageAlbumTitle + '图集')
                if not os.path.exists(ini.path + '/' + imageAlbumTitle):
                    os.makedirs(ini.path + '/' + imageAlbumTitle)
            # 成功爬取数量
            ini.success += 1
        except Exception as e:
            # 异常太多则终止爬取
            if ini.error < 6:
                log_name = ErrorLog(e)
                ini.error += 1
                print('爬取失败，自动跳过: ' + title)
                continue
            else:
                raise Exception('异常太多，终止爬取！')
        if ini.video_count%10==0:
            # 写入表格
            df = pd.DataFrame(DouYinData, columns=['Title', 'Comment', 'LikeNum', 'CommentNum', 'CollectNum', 'RetransmissionNum', 'VideoUrl'])
            df.to_excel('douyin_data.xlsx', index=False)
    # 快速爬取
    if ini.quickDownload:
        if ini.downloaded:
            print('*****************  已爬取完最近更新视频，后续内容跳过  *********************')
            ini.end()
            return
    # 判断作品是否爬取完成
    if not hasMore:
        ini.end()
        return

    print('首页作品爬取完成，将自动滚动屏幕，加载作品，程序检测到新作品后会开始爬取')
    ini.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    # 爬取后续加载的作品
    CrawlerByURL(ini, '/aweme/v1/web/aweme/post/',DouYinData)


# 爬取喜欢作品
def Like(ini, *url):
    ini.url = url[0] if len(url) else input('请输入用户主页链接：')

    # 打开页面，通过人机认证
    print('*****************  请配合开展人机验证，然后等待数据读取及处理  *********************')
    GetWebdriver(ini)
    ini.driver.get(ini.url)
    WebDriverWait(ini.driver, 30).until(ec.title_contains('抖音'))
    time.sleep(5)
    # 爬虫数据list
    DouYinData = []
    # 获取cookies
    GetCookies(ini)

    # 处理首页数据
    data = GetFrontPageData(ini)

    # 数据节点的这个数字会变，所以直接查
    key = [a for a in data if 'uid' in data[a]][0]
    ini.authorName = ini.replace(data[key]["user"]["user"]["nickname"])

    ini.path = f'video/喜欢/{ini.authorName}'
    # 创建文件夹
    if not os.path.exists(ini.path):
        os.makedirs(ini.path)
    print('*****************  跳转喜欢页面  *********************')
    ini.driver.get(ini.driver.current_url + '?showTab=like')
    time.sleep(5)

    # 爬取后续加载的作品
    CrawlerByURL(ini, '/aweme/v1/web/aweme/favorite/',DouYinData)


# 爬取合集作品
def Collection(ini, *url):
    ini.url = url[0] if len(url) else input('请输入视频合集链接：')

    # 打开页面，抓取cookie
    GetWebdriver(ini)
    ini.driver.get(ini.url)
    WebDriverWait(ini.driver, 30).until(ec.title_contains('抖音'))
    time.sleep(5)

    # 获取cookies
    GetCookies(ini)

    # 处理首页数据
    data = GetFrontPageData(ini)

    # 获取合集ID和用户昵称、合集ID、合集名称
    # 数据节点的这个数字会变，所以直接查
    key = [a for a in data if 'mixId' in data[a]][0]
    ini.authorName = ini.replace(data[key]["aweme"]['detail']["authorInfo"]["nickname"])
    mix_id = data[key]['mixId']
    collection_name = ini.replace(data[key]["aweme"]['detail']["mixInfo"]["mixName"])

    # 爬取路径
    ini.path = f'video/合集/{ini.authorName}/{collection_name}'
    # 创建文件夹
    if not os.path.exists(f'video/合集/{ini.authorName}'):
        os.makedirs(f'video/合集/{ini.authorName}')
    if not os.path.exists(ini.path):
        os.makedirs(ini.path)
    print('*****************   开始爬取作品  *********************')
    # 开始执行任务
    while True:
        url = f'https://www.douyin.com/web/api/mix/item/list/?reflow_source=reflow_page&mix_id={mix_id}&count=10&cursor={ini.max_cursor}'
        data = requests.get(url, headers=ini.header).json()
        # 获取作品列表数据
        aweme_list = data['aweme_list']
        CrawlerAweme(ini, aweme_list)
        # 快速爬取
        if ini.quickDownload:
            if ini.downloaded:
                print('*****************  已爬取完最近更新视频，后续内容跳过  *********************')
                ini.end()
                return
        # 判断是否还有下一页
        if data['has_more']:
            # 更新游标
            ini.max_cursor = data['cursor']
        else:
            ini.end()
            return


# 爬取收藏作品
def Favorite(ini):
    ini.url = 'https://www.douyin.com/'

    # 打开页面，抓取cookie
    GetWebdriver(ini)
    ini.driver.get(ini.url)
    WebDriverWait(ini.driver, 30).until(ec.title_contains('抖音'))

    print('*****************  请点击右上角的登录，并在30秒内完成扫码登录  *********************')
    time.sleep(30)

    # 获取cookies
    GetCookies(ini)

    # 处理首页数据
    data = GetFrontPageData(ini)

    # 爬虫数据list
    DouYinData = []

    # 获取用户数据
    ini.authorName = ini.replace(data['1']['user']['info']['nickname'])
    secUid = data['1']['user']['info']['secUid']
    # 构造收藏页面链接
    url = 'https://www.douyin.com/user/' + secUid + '?showTab=favorite_collection'
    ini.driver.get(url)
    time.sleep(5)

    # 爬取路径
    ini.path = f'video/收藏/{ini.authorName}'
    # 创建文件夹
    if not os.path.exists(ini.path):
        os.makedirs(ini.path)

    # 爬取后续加载的作品
    CrawlerByURL(ini, '/aweme/v1/web/aweme/listcollection/',DouYinData)


# 批量爬取
def MultipleDownload(ini):
    # 读取爬取清单
    with open('DownloadList.txt', 'r', encoding='utf-8') as f:
        print('*****************  读取爬取清单  *****************')
        for line in f.readlines():
            if not line.startswith('#'):
                choice = line.split(' ', 1)[0]
                url = line.split(' ', 1)[1].strip('\n')

                if choice == '主页':
                    print(f"*****************  正在爬取 {url} 的主页作品  *****************")
                    Home(ini, url)
                elif choice == '喜欢':
                    print(f"*****************  正在爬取 {url} 的喜欢  *****************")
                    Like(ini, url)
                elif choice == '合集':
                    print(f"*****************  正在爬取 {url} 合集  *****************")
                    Collection(ini, url)
    print('*****************  爬取完成  *****************')

if __name__ == '__main__':
    Start()
