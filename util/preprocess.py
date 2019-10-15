#!/usr/bin/python
# -*- coding: utf-8 -*-

import tldextract


def preprocess(buffer):
    data = []
    for f in buffer:
        try:
            # 1. Split the url,is_malicious
            if f[0] == '\"':  # e.g., '"sgademexico.com/tmp/Inc,Dropbox/1/view.php",1'
                ff = f.strip().split('"')  # e.g., ['', 'sgademexico.com/tmp/Inc,Dropbox/1/view.php', ',1']
                url = ff[1]  # e.g., url = 'sgademexico.com/tmp/Inc,Dropbox/1/view.php'
                is_malicious = ff[2].strip().split(',')[1]  # e.g., is_malicious = '1'

            else:  # e.g., 'www.ourcrazyveterans.com/path/q,1'
                url, is_malicious = f.strip().split(
                    ',')  # e.g., url = 'www.ourcrazyveterans.com/path/q', is_malicous = '1'

            # 2. Split the core domain and cctld
            ext = tldextract.extract(url)
            cctld = ext.suffix.lower()  # cctls = 'com'
            core_domain = '$' + ext.domain.lower() + '$'  # core_domain = 'ourcrazyveterans'

            # 3. Split the netloc
            netloc = url.strip().split('/')[0]  # host = 'www.ourcrazyveterans.com'
            netloc = netloc.lower()

            # 4. Split the path
            url_parse = url.split('/', 1)  # url_parse = ['swopphilly.org']
            if len(url_parse) == 1:
                path = ''
            else:
                path = url_parse[1]

            data.append([url, is_malicious, netloc, core_domain, path, cctld])
        except Exception as e:
            print(str(e))
    if len(data) > 1:
        data.remove(data[0])
    return data


def preprocess_url(url):
    ext = tldextract.extract(url)
    cctld = ext.suffix.lower()  # cctls = 'com'
    core_domain = '$' + ext.domain.lower() + '$'  # core_domain = 'ourcrazyveterans'

    # 3. Split the netloc
    netloc = url.strip().split('/')[0]  # host = 'www.ourcrazyveterans.com'
    netloc = netloc.lower()

    # 4. Split the path
    url_parse = url.split('/', 1)  # url_parse = ['swopphilly.org']
    if len(url_parse) == 1:
        path = ''
    else:
        path = url_parse[1]
    data = [url, netloc, core_domain, path, cctld]

    return data
