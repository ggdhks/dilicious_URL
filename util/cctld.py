#!/usr/bin/python
# -*- coding: utf-8 -*-
import tldextract

'''Attach a unique match TLD'''
class ccTLD():
    def __init__(self):
        self.cctlds = set()
        self.cctlds_tokens = self.get_all_tlds_tokens()

    # add a cctld 
    def add_cctld(self, cctld):
        self.cctlds.add(cctld)

    # match a unique number
    def get_all_tlds_tokens(self):
        tld_tokens = {x: idx + 1 for idx, x in enumerate(self.cctlds)}
        return tld_tokens
