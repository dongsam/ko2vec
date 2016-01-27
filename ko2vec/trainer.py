#-*- coding: utf-8 -*-
__author__ = 'dongsamb'
# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# random
from random import shuffle

# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold

# todo : init from get parameter type of data class object


class AbstractTrainer(object):
    """
    """
    data_list = []
    # data_list_tagged = []

    def __init__(self):
        if self.__class__ is AbstractTrainer:
            raise TypeError('This is abstract class')

    def __len__(self):
        return len(self.data_list)

    def __iter__(self):
        for data in self.data_list:
            yield data

    def __getitem__(self, key):
        return self.data_list[key]


class GensimDoc2VecTrainer(AbstractTrainer):
    """
    """
    # todo: 저장해둔 model 을 불렀을 시 training 없이 진행되도록
    def __init__(self, sources, unsupervised_sources=[], vector_size=300, epoch=10):
        self.sources = sources
        self.unsupervised_sources = unsupervised_sources
        self.vector_size = vector_size
        self.sentences = LabeledSentenceMaker(sources, unsupervised_sources)
        # self.model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
        # self.model = Doc2Vec(self.sentences,
        #     size=vector_size, alpha=0.025, min_alpha=0.025, seed=1234, workers=8)
        self.model = Doc2Vec(
            size=vector_size, alpha=0.025, min_alpha=0.025, seed=1234, workers=8)
        self.model.build_vocab(self.sentences.to_array())

        for epoch in range(epoch):
            self.model.train(self.sentences.sentences_perm())
            self.model.alpha -= 0.002
            self.model.min_alpha = self.model.alpha

    def get_most_similar(self, word):
        return self.model.most_similar(word)

    def save_model(self, file_path):
        self.model.save(file_path)

    # todo: issue : must be called with GensimDoc2VecTrainer instance as first argument
    @classmethod
    def load_model(cls, file_path):
        cls.model = Doc2Vec.load(file_path)
        return cls

    def cross_validation(self, k_fold=5):
        sources_dataset = []

        for source in self.sources:
            for i in source:
                sources_dataset.append(i)

        cross_validation_list = KFold(
            n=len(sources_dataset), n_folds=k_fold, shuffle=True)
        validation_res_list = []
        for train_index_list, test_index_list in cross_validation_list:

            train_arrays = numpy.zeros(
                (len(train_index_list), self.vector_size))
            train_labels = numpy.zeros(len(train_index_list))

            index = 0
            for i in train_index_list:
                train_arrays[index] = self.model.docvecs[sources_dataset[i][2]]
                train_labels[index] = sources_dataset[i][1]
                index += 1

            test_arrays = numpy.zeros((len(test_index_list), self.vector_size))
            test_labels = numpy.zeros(len(test_index_list))

            index = 0
            for i in test_index_list:
                test_arrays[index] = self.model.docvecs[sources_dataset[i][2]]
                test_labels[index] = sources_dataset[i][1]
                index += 1

            classifier = LogisticRegression()
            classifier.fit(train_arrays, train_labels)
            validation_res_list.append(
                classifier.score(test_arrays, test_labels))
            # print classifier.score(test_arrays, test_labels)

        for i, res in enumerate(validation_res_list):
            print("Fold {} :{}".format(str(i+1), str(res)))

        print("Average : {}".format(
            str(sum(validation_res_list)/float(len(validation_res_list)))))


class LabeledSentenceMaker(object):
    """

    """

    def __init__(self, sources, unsupervised_sources=[]):
        self.sources = sources
        self.unsupervised_sources = unsupervised_sources

    def __iter__(self):
        for source in self.sources + self.unsupervised_sources:
            for item_no, row in enumerate(source):
                yield LabeledSentence(words=row[0], tags=[row[2]])

    def to_array(self):
        self.sentences = []
        for source in self.sources + self.unsupervised_sources:
            for item_no, row in enumerate(source):
                # print(row[2])
                self.sentences.append(LabeledSentence(words=row[0], tags=[row[2]]))


        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences
