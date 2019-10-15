#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
3. N-Gram - Feature Engineering
'''
import math
import tldextract
from collections import Counter
from collections import defaultdict
import numpy as np

''' Average '''


def ave(l):
    if len(l) == 0:
        return 0
    else:
        return sum(l) / float(len(l))


'''Bigrams: return a sequence of two adjacent elements from a string'''


def bigrams(words):
    wprev = None
    for w in words:
        if not wprev == None:
            yield (wprev, w)
        wprev = w


'''Trigrams: return a sequence of three adjacent elements from a string'''


def trigrams(words):
    wprev1 = None
    wprev2 = None
    for w in words:
        if not (wprev1 == None or wprev2 == None):
            yield (wprev1, wprev2, w)
        wprev1 = wprev2
        wprev2 = w


def getGramRankDic(nGramTxt):
    gramRankDic = dict()
    for i in nGramTxt:
        category, rank, gram, freq = i.strip().split('\t')  # e.g., 3,21767,ra3,2
        gramRankDic[gram] = int(rank)  # e.g., gramRankDic = {'e':1, 'a':2, ...}
    return gramRankDic


'''Analyze Domain by Unigram, Bigram, Trigram'''


def domainGram(fr):
    unigram_dic = defaultdict(int)  # Create dic object
    bigram_dic = defaultdict(int)
    trigram_dic = defaultdict(int)

    for f in fr:
        url = f.strip().split('\t')[0]
        ext = tldextract.extract(url)
        core_domain = '$' + ext.domain.lower() + '$'  # core_domain = "$google$"

        # defaultdict(int, {'g': 2, 'o': 2, 'l': 1, 'e': 1})
        for i in core_domain[1:-1]:  # "google"
            unigram_dic[i] += 1

            # defaultdict(int, {'$g': 1, 'go': 1, 'oo': 1, 'og': 1, 'gl': 1, 'le': 1, 'e$': 1})
        for i in bigrams(core_domain):
            bigram_dic[''.join(i)] += 1

        # defaultdict(int, {'$go': 1, 'goo': 1, 'oog': 1, 'ogl': 1, 'gle': 1, 'le$': 1})
        for i in trigrams(core_domain):
            trigram_dic[''.join(i)] += 1
    return unigram_dic, bigram_dic, trigram_dic


'''ngram1.txt'''


def writeNgram(fw, unigram_dic, bigram_dic, trigram_dic):
    for rank, (gram, freq) in enumerate(sorted(unigram_dic.items(), key=lambda x: x[1], reverse=True)):
        try:
            fw.write('1\t%d\t%s\t%d\n' % (rank + 1, gram, freq))
        except UnicodeEncodeError:
            continue

    for rank, (gram, freq) in enumerate(sorted(bigram_dic.items(), key=lambda x: x[1], reverse=True)):
        try:
            fw.write('2\t%d\t%s\t%d\n' % (rank + 1, gram, freq))
        except UnicodeEncodeError:
            continue

    for rank, (gram, freq) in enumerate(sorted(trigram_dic.items(), key=lambda x: x[1], reverse=True)):
        try:
            fw.write('3\t%d\t%s\t%d\n' % (rank + 1, gram, freq))
        except UnicodeEncodeError:
            continue


'''ngram2.txt'''


def writeNgram2(fi, fw, gramRankDic):
    fw.write('url\tdomain\tis_malicious\tunigram\tbigram\ttrigram\tcore_domain\n')
    for f in fi:
        url = f.strip().split('\t')[0]
        is_malicious = f.strip().split('\t')[1]
        ext = tldextract.extract(url)
        core_domain = '$' + ext.domain.lower() + '$'  # core_domain = "$google$"

        # 
        unigram_rank = [gramRankDic[i] if i in gramRankDic else 0 for i in core_domain[1:-1]]

        # gramRankDic =          {'go': 1,          'og': 2,          'le': 3}
        # bigram_dic  = {'$g': 1, 'go': 1, 'oo': 1, 'og': 1, 'gl': 1, 'le': 1, 'e$': 1})
        # bigram_rank = [0, 1, 0, 2, 0, 3, 0]
        bigram_rank = [gramRankDic[''.join(i)] if ''.join(i) in gramRankDic else 0 for i in bigrams(core_domain)]

        # 
        trigram_rank = [gramRankDic[''.join(i)] if ''.join(i) in gramRankDic else 0 for i in trigrams(core_domain)]

        try:
            fw.write('%s\t%s\t%.2f\t%.2f\t%.2f\t%s\n' % (
                url, is_malicious, ave(unigram_rank), ave(bigram_rank), ave(trigram_rank), core_domain))
        except UnicodeEncodeError:
            continue

    '''
    domain          class       s1      s2        s3        core 
    google.com.     0           8.00    104.00    512.33    $google$
    facebook.com.   0           9.00    119.00    696.12    $facebook$
    ....
    31060
    '''


def get_rank(gram_rank_dict, core_domain):
    unigram_rank = np.array([gram_rank_dict[i] if i in gram_rank_dict else 0 for i in core_domain[1:-1]])
    bigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in
                            bigrams(core_domain)])  # extract the bigram
    trigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in
                             trigrams(core_domain)])  # extract the bigram


# 1. Open Alexa file, e.g. "1,google.com", apply unigram, bigram, trigram
fr = open('final.txt', 'r')
fr_list = []
for i in fr:
    fr_list.append(i)
fr_list.remove(fr_list[0])
unigram_dic, bigram_dic, trigram_dic = domainGram(fr_list)
fr.close()
print(unigram_dic)
print(bigram_dic)
print(trigram_dic)
# 2. Create output file ngram.txt
'''
ngram-type  rank    string  frequency
1           1       e       90000
2           1       s$      10000
3           1       pus     1000
'''
fw1 = open('ngram_table.csv', 'w')
writeNgram(fw1, unigram_dic, bigram_dic, trigram_dic)
fw1.close()

# # 3. Create gram Rank Dictionary
# nGramTxt = open('ngram_table.csv', 'r')  # e.g., 1,1,e,90878
# gramRankDic = getGramRankDic(nGramTxt)  # e.g., gramRankDic = {'e':1, 'a':2, ...}
# nGramTxt.close()
