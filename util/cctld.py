#!/usr/bin/python
# -*- coding: utf-8 -*-
import tldextract


class ccTLD():
    def __init__(self):
        self.cctlds = set()
        self.cctlds_tokens = self.get_all_tlds_tokens()

    def add_cctld(self, cctld):
        self.cctlds.add(cctld)

    def get_all_tlds_tokens(self):
        tld_tokens = {x: idx + 1 for idx, x in enumerate(self.cctlds)}
        return tld_tokens
