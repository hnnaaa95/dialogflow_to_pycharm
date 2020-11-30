# -*- coding: utf-8 -*-
# import flask dependencies
from flask import Flask, request, make_response, jsonify
import Inference_test
import re
import random

# initialize the flask app
app_test = Flask(__name__)

# default route
@app_test.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    global answer
    # build a request object
    req = request.get_json(force=True)
    response = req.get('queryResult').get('queryText')

    # intent로 발화 지정하기.
    intent = req.get('queryResult').get('intent').get('displayName')
    print(intent)

    # fetch action from json
    #action = req.get('queryResult').get('action')



    if intent == "welcome":

        answer = "안녕하세요"+"\n"+'키스트 임시 진료소에서 코로나 검사를 도와 줄 로봇 바오입니다.\n\
지금부터 코로나 증상 확인을 위한 몇 가지 질문을 드릴테니 정확하게 답변해주시길 바라겠습니다.\n\n\
최근 14일 이내에 해외를 방문한 적 있습니까?'
        response = "Initialization"
        Inference_test.input_SC(response)
        # print(social_cue)
        # print(res_SC)


    else:

        social_cue, res_SC = Inference_test.input_SC(response)
        print(social_cue)
        print(res_SC)


        if intent == "해외방문력":
            answer = res_SC+"\n"+'최근 14일 이내 확진자가 발생한 다중 이용시설이나 장소를 방문한 적 있습니까?.'
        elif intent == "확진자 접촉":
            answer = res_SC+"\n"+'본인 또는 동거인이 최근 14일 이내 코로나 확진자와 접촉한 적 있습니까?'
        elif intent == "체온확인":
            answer = res_SC+"\n"+'저를 쳐다보시면 체온을 측정해드리겠습니다. 화면을 마주보고 계신가요?'
        elif intent == "증상발현유무":
            answer = res_SC+"\n"+"체온은 36.8도입니다."+"최근 7일 이내 관련 증상(발열, 가래, 기침, 숨가쁨, 목통증, 후각/미각 손실, 근육통)이 나타난 적 있습니까?"
        elif intent == "해열제 복용 유무":
            answer = res_SC+"\n"+'해열제를 복용한 적이 있습니까?'
        elif intent == "의사 소견":
            answer = res_SC+"\n"+'답변해주신 내용을 바탕으로 의사의 소견을 듣고 선별진료소 또는 일반진료소에서 진단을 받아야하는지 알려드리겠습니다.'+\
                     "\n진료 결과를 알고 싶으시면 '네'라고 답변 부탁드립니다."
        elif intent == "의사소견 결과":
            dia_result = ['의사의 소견에 따라 선별진료소에서 코로나 검사를 받아주시기 바랍니다.',\
                          '의사의 소견에 따라 일반진료소에서 치료를 받아주시기 바랍니다.']
            answer = res_SC+"\n"+random.choice(dia_result)
        # elif intent == "끝인사":
        #     answer = '이상으로 진료를 마치겠습니다.\n 안녕히 가세요.'
        elif intent == "증상발현유무 - yes":
            answer = res_SC+"\n"+'그러면 증상이 언제부터 나타났습니까?'



    return {'fulfillmentText':answer}

# create a route for webhook
@app_test.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app_test.run()