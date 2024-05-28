
# # 원래 로컬에서 잘 되던 버전
# from openai import OpenAI
# def create_output(text):

#     client = OpenAI(api_key='')

#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "해당 내용을 핵심이 포함되도록 간결하게 요약해주세요"},
#         {"role": "user", "content": text}
#     ]
#     )
#     return completion.choices[0].message.content

'''
# 최신버전 (openai.Completion.create 써야함)
import openai

def create_output(text):
    openai.api_key = ''

    # 대화형 세션용 프롬프트 생성
    prompt_text = f"System: You are a legal expert who must explain as quickly and concisely as possible.\nUser: {text}"

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt_text # 적절한 토큰 수 설정
    )
    # 반환된 결과 접근
    return response.choices[0].text.strip()  # 'message'가 아니라 'text' 속성 사용
'''

import openai

def create_output(text):
    openai.api_key = ''
    base_instruction = "법률 상담에 필요한 내용만 요약해서 알려줘"
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 사용하려는 모델명을 여기에 적습니다.
        messages=[
            {"role": "system", "content": base_instruction},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

def remove_redundancie(text):
    openai.api_key = ''
    base_instruction = '법률 상담에 필요한 말을 제외한 불필요한 말을 제거하고 알려줘'
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 사용하려는 모델명을 여기에 적습니다.
        messages=[
            {"role": "system", "content": base_instruction},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']