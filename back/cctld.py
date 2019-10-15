#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
2. ccTLD/gTLD - Feature Engineering
   generic or country code top-level domain)
'''
import tldextract

'''Attach a best match TLD'''


def addTLD(fr, fw, cctld_dict):
    # Traversing the domain list
    for f in fr:
        # e.g., baidu.jp/p1	0	baidu.jp	$baidu$		p1	jp
        url = f.strip().split('\t')[0]
        is_malicious = f.strip().split('\t')[1]
        ext = tldextract.extract(url)
        cctld = ext.suffix.lower()

        if cctld == '':
            cctld_num = '9999'  # https://12.32.21.33/path
        else:
            if cctld_dict.has_key(cctld):
                # single cctld - single number
                cctld_num = cctld_dict[cctld]
            else:
                cctld_num = 'none'

        # Wtite the output file, add best match TLD
        fw.write('%s\t%s\t%s\t%s\n' % (url, is_malicious, cctld, cctld_num))

    # 1. Open tld file, e.g."uk.com"


tld_file = open('public_suffix_list.txt', 'r')  # com.ac
tld_list = list(t.strip().strip('.') for t in tld_file)
tld_dict = dict((j, i) for i, j in enumerate(tld_list))  # {'ac': 0,'com.ac': 1,'edu.ac': 2,'gov.ac': 3,'net.ac': 4,
tld_file.close()
# print(tld_dict)

# 2. Add the matched ccTLD 
# fr = open('domain250k.txt','r')          # sina.com.cn.	0
fr = open('ds_2m_p.txt', 'r')  # sina.com.cn.	0
fw = open('cctld.txt', 'w')  # output file
addTLD(fr, fw, tld_dict)  # sina.com.cn.	0	.com.cn.
fw.close()
fr.close()
