# coding=utf-8
import re
import requests


def lofterspider(username):
    url_cmp = re.compile('<img[^>]+src="(.+?)"', re.S)
    url = 'http://%s.lofter.com/' % name
    outputfile = open(str(username) + r'lofter.txt', 'w')
    num = 0
    page_num = 1
    try:
        while True:
            page_url = url + '?page=' + str(page_num)
            html_cont = requests.get(page_url)
            pic_urls = re.findall(url_cmp, html_cont.content)
            pic_urls.pop(0)
            if len(pic_urls) == 0:
                break
            print page_url
            for pic_url in pic_urls:
                pic_url = pic_url.split('?', 1)[0]
                outputfile.write(pic_url + '\n')
                num += 1
            page_num += 1
    finally:
        outputfile.close()
    print r'Finished! Crawl {0} link!'.format(str(num))


def doubanspider(album):
    url_cmp = re.compile(r'<a href="(.+?)"(?=[^>]class="photolst_photo")')
    pic_cmp = re.compile(r'(?<=<a href="#" class="view-zoom view-zoom-out"><img src=").+?(?=")', re.S)
    album_url = 'https://www.douban.com/photos/album/%s/?start=' % album
    start, num = 0, 0
    lis = []

    while True:
        url = album_url + str(start)
        print url
        cont = requests.get(url)
        pic_urls = re.findall(url_cmp, cont.content)
        for pic_url in pic_urls:
            new_url = pic_url + 'large'
            pic_cont = requests.get(new_url)
            large_url = re.findall(pic_cmp, pic_cont.content)
            lis.append(large_url[0])
            num += 1
        if len(pic_urls) < 18:
            break
        else:
            start += 18

    pic = set(lis)
    outputfile = open(str(album) + r'douban.txt', 'w')
    for i in pic:
        outputfile.write(i + '\n')
    outputfile.close()
    print r'Finished! Crawl {0} links!'.format(str(num))

def tumblrspider(name):
    url_cmp = re.compile(r'(?<=<photo-url max-width="1280">).+?(?=</photo-url>)', re.S)
    api_url = 'https://%s.tumblr.com/api/read?type=photo&num=50&start=' % name
    outputfile = open(str(name) + r'tumblr.txt', 'w')
    start, num = 0, 0
    try:
        while True:
            url = api_url + str(start)
            print url
            xml_cont = requests.get(url, timeout=100)
            pic_urls = re.findall(url_cmp, xml_cont.content)
            pic_urls = list(set(pic_urls))
            for pic_url in pic_urls:
                outputfile.write(pic_url + '\n')
                num += 1
            if len(pic_urls) < 50:
                break
            else:
                start += 50
    except:
        print 'something wrong!'
    finally:
        outputfile.close()
    print r'Finished! Crawl {0} links!'.format(str(num))

tip = '''请输入LOFTER或tumblr用户名或豆瓣相册编号：
例如：lofter username或者douban 1234567890\n'''
inputstr = raw_input(tip)

arr = inputstr.split(' ')
site = arr[0]
name = arr[1]
if site=='lofter':
    lofterspider(name)
elif site=='douban':
    doubanspider(name)
elif site=='tumblr':
    tumblrspider(name)
else:
    print 'Please enter right address!'
