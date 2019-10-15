#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
3. N-Gram - Feature Engineering
'''
import math
import tldextract
import numpy as np
from collections import defaultdict

''' Calculate the standard value '''


def std(list_):
    if len(list_) > 0:
        return list_.std()  # standard value
    else:
        return 0  # Remove Nan, set Nan to 0


''' Calculate the mean value '''


def ave(list_):
    if len(list_) > 0:
        return list_.mean()  # average value
    else:
        return 0  # Remove Nan, set Nan to 0


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
    for rank, (gram, freq) in enumerate(sorted(unigram_dic.iteritems(), key=lambda x: x[1], reverse=True)):
        try:
            fw.write('1\t%d\t%s\t%d\n' % (rank + 1, gram, freq))
        except UnicodeEncodeError:
            continue

    for rank, (gram, freq) in enumerate(sorted(bigram_dic.iteritems(), key=lambda x: x[1], reverse=True)):
        try:
            fw.write('2\t%d\t%s\t%d\n' % (rank + 1, gram, freq))
        except UnicodeEncodeError:
            continue

    for rank, (gram, freq) in enumerate(sorted(trigram_dic.iteritems(), key=lambda x: x[1], reverse=True)):
        try:
            fw.write('3\t%d\t%s\t%d\n' % (rank + 1, gram, freq))
        except UnicodeEncodeError:
            continue


def get_rank(gram_rank_dict, core_domain):
    unigram_rank = np.array([gram_rank_dict[i] if i in gram_rank_dict else 0 for i in core_domain[1:-1]])
    bigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in
                            bigrams(core_domain)])  # extract the bigram
    trigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in
                             trigrams(core_domain)])  # extract the bigram
    return [ave(unigram_rank), ave(bigram_rank), ave(trigram_rank), std(unigram_rank), std(bigram_rank),
            std(trigram_rank)]


def get_gram_rank_dict(buffer):
    gram_rank_dict = dict()
    for i in buffer:
        category, rank, gram, freq = i.strip().split('\t')  # e.g., 3,21767,ra3,2
        gram_rank_dict[gram] = int(rank)  # e.g., gramRankDic = {'e':1, 'a':2, ...}
    return gram_rank_dict
