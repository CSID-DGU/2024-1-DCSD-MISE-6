from OCR_image import *
from text_summarize import *
from create_answer import * 
import imghdr
import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random 
import imghdr
import os
from rag import *
import warnings
warnings.filterwarnings('ignore')



def is_image(file_path):
    """
    이미지인지 확인 하는 함수
    """
    image_formats = ['jpeg', 'png', 'gif', 'bmp', 'tiff']
    format = imghdr.what(file_path)
    return format in image_formats

def classify_input(input_data):
    """
    텍스트인지 이미지인지 구분 / 이미지는 경로로 들어오는 것으로 예상
    """
    if os.path.isfile(input_data):
        if is_image(input_data):
            result = detect_text(input_data, '경로')  # TODO key는 구글 비전 키가 들어가야함
            result = translate_text(result)
            return result
    return input_data

application = Flask(__name__)

@application.route("/", methods=['POST'])
def keyword():
    req = request.get_json()
    text_ck = req['userRequest']['utterance']
    text_out = classify_input(text_ck)
    before_text = process_query(text_out)
    text = create_output(before_text)
    

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
    return jsonify(res)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
