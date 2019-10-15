#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
4. Feature Extractor
'''
import math
import pickle
import tldextract
import numpy as np
import gib_detect_train
from itertools import groupby
from ngram import bigrams, trigrams, getGramRankDic
from collections import Counter, defaultdict
from entropy import std, ave, count_vowels, count_digits, count_repeat_letter, consecutive_digits, \
    consecutive_consonant, shannonEntropy

# n-gram
nGramTxt = open('ngram1.txt', 'r')
gram_rank_dict = getGramRankDic(nGramTxt)  # e.g., gram_rank_dict = {'e':1, 'a':2, ...}
nGramTxt.close()

# Gibberish detector
model_data = pickle.load(open('gib_model.pki', 'rb'))
model_mat = model_data['mat']
threshold = model_data['thresh']

# set heaader
fw = open('feature1.txt', 'w')
# header = 'domain\tclass\ttld\tentropy\tlen\tnorm_entropy\tvowel_ratio\tdigit_ratio\trepeat_letter\tconsec_digit\tconsec_consonant\tuni_rank\tbi_rank\ttri_rank\tuni_std\tbi_std\ttri_std\tgib_value\n'
header = 'url\tis_malicious\tcctld_num\tentropy\tlength\tnorm_entropy\tuni_rank\tbi_rank\ttri_rank\tuni_std\tbi_std\ttri_std\tgib_value\n'
# header = 'url\tdomain\tcore_domain\tis_malicious\tentropy1\tlength1\tn_entropy1\tentropy2\tlength2\tn_entropy2\tentropy3\tlength3\tn_entropy3\n'
fw.write('%s' % (header))

fi = open('cctld.txt',
          'r')  # e.g., myspace.com/everything/leonard-cohen 0   myspace.com $myspace$   everything/leonard-cohen    com
for f in fi:
    url, is_malicious, cctld, cctld_num = f.strip().split('\t')

    # host
    host = url.strip().split('/')[0]  # host = 'www.ourcrazyveterans.com'
    host = host.lower()

    ext = tldextract.extract(url)
    core_domain = '$' + ext.domain.lower() + '$'  # core_domain = "$google$"

    # 1. Shannon entropy feature

    # 1.1 url
    # new_url = url.strip().split('://')[1]               # 'http://forum.woltlab.fr/commu/path1'
    # new_url = new_url[:-1]
    f_len1, count1, entropy1 = shannonEntropy(url)  # 'forum.woltlab.fr/commu/path1'

    # 1.2 host
    # f_len2, count2, entropy2 = shannonEntropy(host)        # forum.woltlab.fr

    # 1.3 core domainn
    # f_len3, count3, entropy3 = shannonEntropy(core_domain) # woltlab

    # vowel_ratio = count_vowels(core_domain)/f_len
    # digit_ratio = count_digits(core_domain)/f_len
    # repeat_letter = count_repeat_letter(core_domain)/f_len
    # consec_digit = consecutive_digits(core_domain)/f_len
    # consec_consonant = consecutive_consonant(core_domain)/f_len

    # 2. N-Gram Feature

    unigram_rank = np.array([gram_rank_dict[i] if i in gram_rank_dict else 0 for i in host[1:-1]])
    bigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in
                            bigrams(host)])  # extract the bigram
    trigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in
                             trigrams(host)])  # extract the bigram

    # 3. Gib_value Feature
    gib_value = int(gib_detect_train.avg_transition_prob(host, model_mat) > threshold)

    try:
        fw.write('%s\t%s\t%s\t%.3f\t%.1f\t%.3f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n'
                 % (url, is_malicious,
                    cctld_num,
                    entropy1, f_len1, entropy1 / f_len1,
                    # vowel_ratio,digit_ratio,repeat_letter,consec_digit,consec_consonant,
                    ave(unigram_rank), ave(bigram_rank), ave(trigram_rank),
                    std(unigram_rank), std(bigram_rank), std(trigram_rank),
                    gib_value))

    except UnicodeEncodeError:
        continue

fw.close()
fi.close()
