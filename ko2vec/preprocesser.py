#-*- coding: utf-8 -*-
__author__ = 'dongsamb'
import json
import nltk

# todo: inherit from loader, and return data class object


class AbstractPreprocessor(object):
    """

    """
    data_list_tagged = []
    tokens = []
    nltk_tokens = []

    def __init__(self):
        if self.__class__ is AbstractPreprocessor:
            raise TypeError('This is abstract class')

    def __len__(self):
        return len(self.data_list_tagged)

    def __iter__(self):
        for data_tagged in self.data_list_tagged:
            yield data_tagged

    def __getitem__(self, key):
        return self.data_list_tagged[key]

    def pprint(self):
        print(json.dumps(self.data_list_tagged, ensure_ascii=False))

    def __str__(self):
        return json.dumps(self.data_list_tagged, ensure_ascii=False)

    def top(self, count=10):
        if not self.tokens:
            self.tokens = [
                data for row in self.data_list_tagged for data in row[0]]
        if not self.nltk_tokens:
            self.nltk_tokens = nltk.Text(self.tokens, name='NMSC')
        for token in self.nltk_tokens.vocab().most_common(count):
            yield token

    def count_tokens(self):
        if not self.tokens:
            self.tokens = [
                data for row in self.data_list_tagged for data in row[0]]
        if not self.nltk_tokens:
            self.nltk_tokens = nltk.Text(self.tokens, name='NMSC')
        return len(self.nltk_tokens.tokens)

    def count_unique_tokens(self):
        if not self.tokens:
            self.tokens = [
                data for row in self.data_list_tagged for data in row[0]]
        if not self.nltk_tokens:
            self.nltk_tokens = nltk.Text(self.tokens, name='NMSC')
        return len(set(self.nltk_tokens.tokens))

    @staticmethod
    def _tokenize(pos_tagger, data):
        return [t[0] for t in pos_tagger.pos(data)]
        # return ['/'.join(t) for t in pos_tagger.pos(data)]

class TwitterTagging(AbstractPreprocessor):
    """

    """

    def __init__(self, loader, jvmPath=''):
        from konlpy.tag import Twitter
        if not jvmPath:
            jvmPath = "/Library/Java/JavaVirtualMachines/jdk1.8.0_66.jdk/Contents/Home/jre/lib/server/libjvm.dylib"
        try:
            pos_tagger = Twitter(jvmPath)
        except:
            print('input jvmPath of your environment')
            print('''ex) TwitterTagging(my_loader, jvmPath='/Library/Java/my/libjvm/Path...' ''')

        try:
            self.data_list_tagged = [
                (self._tokenize(pos_tagger, row[0]), row[1], row[2]) for row in loader]
        except:
            self.data_list_tagged = [
                (self._tokenize(pos_tagger, row[0])) for row in loader]

    @staticmethod
    def _tokenize(pos_tagger, data):
        return ['/'.join(t) for t in pos_tagger.pos(data, norm=True, stem=True)]


class MecabTagging(AbstractPreprocessor):
    # todo: install mecab = bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
    def __init__(self, loader):
        try:
            from konlpy.tag import Mecab
            pos_tagger = Mecab()
        except Exception as e:
            print('need to install mecab, using below command')
            print('bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)')

        try:
            self.data_list_tagged = [
                (self._tokenize(pos_tagger, row[0]), row[1], row[2]) for row in loader]
        except:
            self.data_list_tagged = [
                (self._tokenize(pos_tagger, row[0])) for row in loader]


# todo : 형태소분석 도중 상장사같은 키워드가 있으면 분리 안하도록 예외처리 필요