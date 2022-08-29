import logging
import gensim
import numpy as np


class Sentence2vecModel:
    try:
        model = gensim.models.Word2Vec.load('path-to-vectors.txt', binary=False)
        sentence = ["London", "is", "the", "capital", "of", "Great", "Britain"]
        vectors = [model[w] for w in sentence]
    except Exception as e:
        logging.exception(e)

    def sent2vec(self, words):
        if (len(words) == 0):
            return []
        temp = []
        for word in words:
            if word in Sentence2vecModel.model:
                temp.append(Sentence2vecModel.model[word])
        if len(temp) == 0:
            return []
        return np.average(temp, axis=0)