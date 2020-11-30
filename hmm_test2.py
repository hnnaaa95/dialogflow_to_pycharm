import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pomegranate import *
from pomegranate.callbacks import CSVLogger, ModelCheckpoint
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import pandas as pd
from pandas import DataFrame, Series


class social_dialogue:

    def predict_hmm(input_cue):
        # Load model
        with open('/home/kist/catkin_ws/src/hnna_pkg_test/data/hmm_save_viterbi', 'rb') as fp:
            hmm_model = pickle.load(fp)

        SC = {'s2': 'self-disclosure elicitation', 's3': 'self-disclosure', 's4': 'suggestion', 's5': 'general statement',
                  's6':'yesno', 's7':'acknowledgement', 's8': 'praise'}

        #model predict
        predict = [state.name for i, state in hmm_model.viterbi(input_cue)[1]][1:]
        # print("predict[-1]: ", predict[-1])
        # print("str([SC[i] for i in predict])",str([SC[i] for i in predict]))


        # generate sentence
        social_cue_sen = \
            {'None': "없음",
             'Greetings': "안녕하세요.",
             's2': "",
             's5': random.choice(["전염 예방을 위해서는 정확한 답변이 도움된다고 합니다.",
                                  "코로나 관련 증상이 나타날 때는 외출을 삼가하는 것도 하나의 방법 입니다.",
                                  "코로나 생활 수칙을 알고 지키는 것은 중요합니다."]),
             's6': random.choice(["네.","예."]),
             's7': random.choice(["그러시군요.", "그랬군요."]),
             's8': random.choice(["말씀해 주셔서 감사합니다.","감사합니다.","알려주셔서 감사합니다.","성실한 답변 감사합니다."]),
             'Termination': "안녕하세요."}

        return str([SC[i] for i in predict]),social_cue_sen[predict[-1]]






