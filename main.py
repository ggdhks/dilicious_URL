#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import csv
from util import preprocess
from util import cctld
from util import entropy
from util import ngram
from util import gib_detect_train
from pprint import pprint

data_file_name = 'final.txt'
processed_data = 'featured.csv'


def preprocess_data(filename):
    with open(filename, 'r') as f:
        return preprocess.preprocess(f)


def preprocess_url(data):
    return preprocess.preprocess_url(data)


def read_ngram_table_dict():
    fr_list = []
    with open('ngram_table.txt', 'r') as f:
        for i in f:
            fr_list.append(i)
        fr_list.remove(fr_list[0])
        return ngram.get_gram_rank_dict(fr_list)


def read_gib_model():
    model_data = pickle.load(open('gib_model.pki', 'rb'))
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return model_mat, threshold


def save_file(data):
    with open(processed_data, mode='w') as csv_file:
        fieldnames = ['url', 'is_malicious', 'host', 'core_domain', 'path', 'cctld_number', 'url_entropy', 'url_length',
                      'path_entropy', 'path_length', 'unigram_avg', 'bigram_avg', 'trigram_avg', 'unigram_std',
                      'bigram_std', 'trigram_std', 'gib_value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in data:
            writer.writerow(
                {
                    'url': i[0],
                    'is_malicious': i[1],
                    'host': i[2],
                    'core_domain': i[3],
                    'path': i[4],
                    'cctld_number': i[5],
                    'url_entropy': i[6],
                    'url_length': i[7],
                    'path_entropy': i[8],
                    'path_length': i[9],
                    'unigram_avg': i[10],
                    'bigram_avg': i[11],
                    'trigram_avg': i[12],
                    'unigram_std': i[13],
                    'bigram_std': i[14],
                    'trigram_std': i[15],
                    'gib_value': i[16]
                }
            )


def get_feartures(url):
    preprocessed_data = preprocess_url(url)
    cctld_object = cctld.ccTLD()
    ngram_table_dict = read_ngram_table_dict()
    model_mat, threshold = read_gib_model()

    preprocessed_data[-1] = 1  # cctld number
    url_entropy = list(entropy.shannon_entropy(preprocessed_data[0]))
    path_entropy = list(entropy.shannon_entropy(preprocessed_data[3]))
    preprocessed_data.extend(url_entropy)
    preprocessed_data.extend(path_entropy)
    ranks = ngram.get_rank(ngram_table_dict, preprocessed_data[2])
    preprocessed_data.extend(ranks)
    gib_value = int(gib_detect_train.avg_transition_prob(preprocessed_data[1], model_mat) > threshold)
    preprocessed_data.append(gib_value)
    final_data = []
    final_data.extend(url_entropy)
    final_data.extend(path_entropy)
    final_data.extend(ranks)
    final_data.append(gib_value)
    return final_data


def main():
    preprocessed_data = preprocess_data(data_file_name)
    cctld_object = cctld.ccTLD()
    ngram_table_dict = read_ngram_table_dict()
    model_mat, threshold = read_gib_model()
    for i in preprocessed_data:
        cctld_object.add_cctld(i[-1])
    cctld_tokens = cctld_object.get_all_tlds_tokens()

    for i in preprocessed_data:
        try:
            i[-1] = cctld_tokens[i[-1]]
            # url_shannon_entropy, url_length, url_norm_entropy
            url_entropy = list(entropy.shannon_entropy(i[0]))
            # path_shannon_entropy, path_length, path_norm_entropy
            path_entropy = list(entropy.shannon_entropy(i[4]))
            i.extend(url_entropy)
            i.extend(path_entropy)
            i.extend(ngram.get_rank(ngram_table_dict, i[3]))
            # print(ngrams_rank_std)
            gib_value = int(gib_detect_train.avg_transition_prob(i[2], model_mat) > threshold)
            i.append(gib_value)
        except:
            print(i)
    save_file(preprocessed_data)


if __name__ == '__main__':
    print(get_feartures('baidu.com'))
    # pprint(ngram.caculate_domain_gram('baidubaidahudfjdhklsfjhjbv.com'))
