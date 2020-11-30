# default packages


import pickle
import numpy as np
import threading
import argparse
import re
import os

# Preprocessing packages
from koalanlp.Util import initialize
from koalanlp.proc import Tagger
from koalanlp import API

#Embedding packages
from gensim.models.doc2vec import Doc2Vec

# Classifier packages
from sklearn.naive_bayes import GaussianNB

class Social_classifier:
    #default model path
    default_embed_model_path = '/home/kist/repository/dialogflow/social_dialog_strategy_classifier/models/default_models/deeptask_Sentence2vector_0_5_100_200'
    default_cls_model_path = '/home/kist/repository/dialogflow/social_dialog_strategy_classifier/models/default_models/clf_NaiveBayes.model'


    social_cue = {0: 'None',
                  1: 'Greetings',
                  2: 'Self-disclosure eliciation',
                  3: 'Self-disclosure',
                  4: 'Suggestion',
                  5: 'General Statement',
                  6: 'Simple yes/no',
                  7: 'Acknowledgement',
                  8: 'Praise',
                  9: 'Termination'}

    def __init__(self, embed_model_path=default_embed_model_path, cls_model_path=default_cls_model_path):
        if not os.path.isfile(embed_model_path):
            print('embed_model doesn\'t exist.\ncheck the model path')
        if not os.path.isfile(cls_model_path):
            print('classifier_model doesn\'t exist.\ncheck the model path')


        # 전처리 패키지 초기화
        print('Init preprocessing')
        initialize(KMR='2.1.4') #LATEST--> 2.1.4로 변경
        self.tagger = Tagger(API.KMR)

        # 임베딩 모델 로딩
        print('Loading Embedding model')
        self.embedding_model = Doc2Vec.load(embed_model_path)

        # Classifier 모델 로딩
        print('Loading Classifier model')
        with open(cls_model_path, 'rb') as fp:
            self.clf_model = pickle.load(fp)

    # sentence input , preprocessed sentence output
    def preprocessing(self, tagger, sentence):
        # 자음, 모음 단독 사용 제거
        sentence = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', sentence)
        sentence.strip()
        # 형태소 태깅
        tagged_string = tagger(sentence)
        analysis_sentence_list = re.split('\s|\+', tagged_string[0].singleLineString())
        # 형태소 분석 후처리
        for i, data in enumerate(analysis_sentence_list):
            if re.findall('/SF|/SP|/SS|/SE|/SO|/SL|/SH|/SW|/NF|/NV|/SN|/NA', data):
                analysis_sentence_list[i] = re.findall('/SF|/SP|/SS|/SE|/SO|/SL|/SH|/SW|/NF|/NV|/SN|/NA', data)[0]

        return analysis_sentence_list

    # sentence input, vector output
    def input_feature_inference(self, model=None, sentence=None):
        # model = Doc2Vec.load("models/deeptask_Sentence2vector_0_8_800_100")
        return model.infer_vector(sentence).reshape(1, model.docvecs.vector_size)

    # vector input, class output
    def infer_classification(self, clf=None, feature=None):
        y_pred = clf.predict(feature)

        return y_pred.item()

    # one sentence input , class output
    def infer(self, input_sentence):

        # preprocessing
        # print(input_sentence)
        preprocessed_sentence = self.preprocessing(self.tagger, input_sentence)
        # print(preprocessed_sentence)

        # embedding
        input_feature = self.input_feature_inference(model=self.embedding_model, sentence=preprocessed_sentence)
        # print(input_feature)

        # classification
        social_cue = self.infer_classification(self.clf_model, input_feature)

        return social_cue


