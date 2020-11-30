import social_classifier
social_cue =  {0:'None',
               1:'Greetings' ,
               2:'Self-disclosure eliciation' ,
               3:'Self-disclosure' ,
               4:'Suggestion',
               5:'General Statement',
               6:'Simple yes/no',
               7:'Acknowledgement',
               8:'Praise',
               9:'Termination'}


#


clf = social_classifier.Social_classifier()

import hmm_test2

# global input_cue
input_cue = []

# 추론 문장 입력
def input_SC(input_sentence):

    if input_sentence == "Initialization":
        input_cue.clear()

    else:
        print("input_sentence: ", input_sentence)
        print("Human's social cue: ", social_cue[clf.infer(input_sentence)])

        if clf.infer(input_sentence) == 9:
            return "Termination", "대화를 종료합니다."

        else:
            input_cue.append(clf.infer(input_sentence))
            return hmm_test2.social_dialogue.predict_hmm(input_cue)



