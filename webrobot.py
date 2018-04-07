#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'van1988ch'

import urllib2
import re
import urlparse
from datetime import datetime
import time

class Throttle:
    """限速,每个域名一个计时器
    """
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}
        
    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


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
    seen = set(crawl_queue)
    throttle = Throttle(3)
    while crawl_queue:
        url = crawl_queue.pop()
        throttle.wait(url)
        html = Download(url)
        if html:
            for link in get_links(html):
                link = urlparse.urljoin(seed_url, link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)


def get_links(html):
    """正则匹配分析出所有的链接
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

if __name__ == '__main__':
    link_crawler('http://www.iplaysoft.com/')