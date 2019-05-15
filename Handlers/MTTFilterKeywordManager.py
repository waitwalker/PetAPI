# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 2:15 PM
# @Author  : waitWalker
# @Email   : waitwalker@163.com
# @File    : MTTFilterKeywordManager.py
# @Software: PyCharm
import os
import json
import marisa_trie
import sys
from functools import lru_cache
import logging as log

class MTTFilterKeywordManager(object):

    def __init__(self, words):
        self.sensitive_words = words


    def get_trie(self):
        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path))
        file_path = father_path + "/files/keyword.txt"
        words = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                words.append(line.strip('\n'))
        trie = marisa_trie.Trie(words)
        return trie

    def filter_word(self, trie, content):
        result = []
        i = 0
        while True:
            # log.debug(content[i:])
            filter_word = trie.prefixes(content[i:])
            if not content[i:]:
                break
            # log.debug(filter_word)
            if filter_word:
                current_filter_word_max_len = len(sorted(filter_word, key=lambda k: len(k), reverse=True)[0])
                i = i + current_filter_word_max_len
                result.extend(filter_word)
            else:
                i = i + 1
        # log.debug(get_trie.cache_info())
        # log.debug(','.join(list(set(result))))
        print("result count:", len(result))
        if len(result) > 0:
            return True
        else:
            return False

    def replace_word(self, trie, content):
        result = []
        i = 0
        while True:
            # log.debug(content[i:])
            filter_word = trie.prefixes(content[i:])
            if not content[i:]:
                break
            # log.debug(filter_word)
            if filter_word:
                current_filter_word_max_len = len(sorted(filter_word, key=lambda k: len(k), reverse=True)[0])
                i = i + current_filter_word_max_len
                result.extend(filter_word)
            else:
                i = i + 1
        # log.debug(get_trie.cache_info())
        # log.debug(','.join(list(set(result))))
        print("result count:", len(result))
        return result






