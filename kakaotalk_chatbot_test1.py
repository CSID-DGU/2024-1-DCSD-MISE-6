from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random 

application = Flask(__name__)  

@application.route("/", methods=['POST'])
def keyword():    
	req = request.get_json()    
	text_ck = req['userRequest']['utterance']    
	text = '정보를 찾을 수 없습니다'     

	text = text_ck*3

	# 답변 텍스트 설정    
	res = {
	        "version": "2.0",
			"template": {
				"outputs": [                
					{
						"simpleText": {
							"text": text
							}
						}
					]
				}
			}     
	
	# 답변 전송    
	return jsonify(res)  

if __name__ == "__main__":
	application.run(host='0.0.0.0', port=5000, threaded=True)
