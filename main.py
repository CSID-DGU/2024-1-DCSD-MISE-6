from OCR_image import *
from text_summarize import *
import imghdr
import os


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
            # result = detect_text(input_data, key) #TODO key는 구글 비전 키가 들어가야함
            # result = translate_text(result)
            return 'image'
    else:
        return input_data

if __name__ == "__main__":
    user_input = input("input??")
    text_out = classify_input(user_input)
    print(text_out)