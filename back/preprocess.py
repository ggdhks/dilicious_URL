#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
0. Preprocess the data file
	
	Original:
	url is_malicous

	Modified:
	url is_malicous host core_domain path cctld
'''
import tldextract


def urlSplit(fr, fw):
    for f in fr:
        # 1. Split the url,is_malicious
        if f[0] == '\"':  # e.g., '"sgademexico.com/tmp/Inc,Dropbox/1/view.php",1'
            ff = f.strip().split('"')  # e.g., ['', 'sgademexico.com/tmp/Inc,Dropbox/1/view.php', ',1']
            url = ff[1]  # e.g., url = 'sgademexico.com/tmp/Inc,Dropbox/1/view.php'
            is_malicious = ff[2].strip().split(',')[1]  # e.g., is_malicious = '1'

        else:  # e.g., 'www.ourcrazyveterans.com/path/q,1'
            url, is_malicious = f.strip().split(',')  # e.g., url = 'www.ourcrazyveterans.com/path/q', is_malicous = '1'

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

        try:
            fw.write('%s\t%s\t%s\t%s\t%s\t%s\n'
                     % (url, is_malicious, netloc, core_domain, path, cctld))
        except UnicodeEncodeError:
            continue

# Collect cctld
def suffixDic(fr, fw):
    for f in fr:
        # remove comment
        if f[0] == "/":
            continue
        # remove empty line
        data = f.strip()
        if len(data) != 0:
            fw.write(f)

        # 1. Split url


fr = open('ds_2m.txt', 'r')  # e.g., youtube.com/watch?v=sC8hOIjwZYY,0
fw = open('ds_2m_p.txt', 'w')
urlSplit(fr, fw)  # e.g., youtube.com/watch?v=jiUY1UNCxI4	0	youtube.com	$youtube$	watch?v=jiUY1UNCxI4	com
fw.close()
fr.close()
'''
Test: 
swopphilly.org,1
fr-mobile.net/FR/c5ef1ba3618bd70,0
www.baidu.com,0
"sgademexico.com/tmp/Inc,Dropbox/1/view.php",1

swopphilly.org	1	swopphilly.org	$swopphilly$		org
fr-mobile.net/FR/c5ef1ba3618bd70	0	fr-mobile.net	$fr-mobile$	FR/c5ef1ba3618bd70	net
www.baidu.com	0	www.baidu.com	$baidu$		com
sgademexico.com/tmp/Inc,Dropbox/1/view.php	1	sgademexico.com	$sgademexico$	tmp/Inc,Dropbox/1/view.php	com
'''

'''
# 2. Create cctld dictionary
fr1 = open('public_suffix_original.txt','r')  
fw1 = open('public_suffix_list.txt','w') 
suffixDic(fr1, fw1)
fw1.close()
fr1.close()

dynvpn.de
mein-vigor.de
my-vigor.de
my-wan.de
syno-ds.de
...
'''
