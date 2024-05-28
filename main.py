from OCR_image import *
from text_summarize import *
from create_answer import *
#import imghdr
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
from PIL import Image
from flask import Flask, request, jsonify
import requests
import threading
import time
from model_ans import *


def is_image(file_path):
    """
    파일이 지원하는 이미지 형식 중 하나인지 확인하는 함수
    """
    image_formats = ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF']
    try:
        with Image.open(file_path) as img:
            return img.format in image_formats
    except IOError:
        # 파일이 이미지가 아니거나 손상된 경우
        return False


def classify_input(input_data):
    """
    텍스트인지 이미지인지 구분 / 이미지는 경로로 들어오는 것으로 예상
    """
    if os.path.isfile(input_data):
        if is_image(input_data):
            result = detect_text(input_data, 'json_path.json')  # TODO key는 구글 비전 키가 들어가야함
            result = translate_text(result)
            return result
    return input_data
def send_callback_response(callback_url, text):
    """비동기 처리 후 콜백 URL로 결과를 보내는 함수."""
    callback_data = {
        "version": "2.0",
        "useCallback": True,
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
    try:
        response = requests.post(callback_url, json=callback_data)
        response.raise_for_status()
        print(f"Callback succeeded: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send callback: {e}")


application = Flask(__name__)

def send_callback_response(callback_url, text):
    """비동기 처리 후 콜백 URL로 결과를 보내는 함수."""
    callback_data = {
        "version": "2.0",
        "useCallback": True,
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
    response = requests.post(callback_url, json=callback_data)
    print("Callback POST response:", response.status_code, response.text)

def process_request_async(text_ck, callback_url):
    """비동기로 긴 처리 과정을 수행하고 콜백 URL을 통해 결과를 전송하는 함수."""
    try:
        text_out = classify_input(text_ck)  # 입력 분류
        rag_text = process_query(text_out)  # 최종 처리
        ing_text = model_answer(text_ck,rag_text) # 라마 
        final_text = remove_redundancie(ing_text)
        # final_text = create_output(rag_text)
        send_callback_response(callback_url, final_text)  # 콜백 URL로 결과 전송
    except Exception as e:
        print(f"Error in processing request asynchronously: {e}")


@application.route("/keyword", methods=['POST'])
def keyword():
    req = request.get_json()
    text_ck = req['userRequest']['utterance']
    callback_url = req['userRequest'].get('callbackUrl')

    if callback_url:  # 콜백 URL이 제공되면 비동기 처리를 시작
        threading.Thread(target=process_request_async, args=(text_ck, callback_url)).start()
        return jsonify({
            "version": "2.0",
            "useCallback": True,
            "data": {
                "text": "답변 생성중 "
            }
        })
    else:
        final_text = "다시질문해주세요"
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": final_text
                        }
                    }
                ]
            }
        })

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
