import openai
import pandas as pd

# OpenAI API 키 설정
openai.api_key = 'key'

def translate_text(text):
    command = "해당 내용을 한국어로 간결하게 요약하여 문제의 핵심만 포함하도록 하세요. 불필요한 날짜, 개인 정보는 제거하세요."
    content = f"{text} {command}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a legal expert who must explain as quickly and concisely as possible."},
                {"role": "user", "content": content},
            ]
        )
        translated_text = response['choices'][0]['message']['content']
        return translated_text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# 사용 방법
# filter_texts = translate_text(text)

