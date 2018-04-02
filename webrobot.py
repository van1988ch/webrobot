#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'van1988ch'

import urllib2

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
    return html

print Download("http://www.baidu.com")