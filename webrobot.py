#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'van1988ch'

import urllib2
import re

def Download(url, retrynum=2):
    """抓取网页, retrynum=[500,600)错误重试次数"""
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if retrynum > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                html = Download(url, retrynum-1)
    except :
        html = None
    return html

def link_crawler(seed_url):
    """分析网页中的内部链接来抓取全部网页
    """
    crawl_queue = [seed_url] 
    while crawl_queue:
        url = crawl_queue.pop()
        html = Download(url)
        if html:
            for link in get_links(html):
                crawl_queue.append(link)


def get_links(html):
    """正则匹配分析出所有的链接
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

if __name__ == '__main__':
    link_crawler('http://www.iplaysoft.com/')