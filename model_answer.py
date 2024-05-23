import transformers
import bitsandbytes
import json
import requests
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

app = Flask(__name__)

model_id = "JianKim3293/llama3-KoEn-8B-Instruct-law"

compute_dtype = torch.float16
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False
)

# 토크나이저 및 모델 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token  # 패딩 토큰 설정

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=quant_config,
    device_map="auto",
    safe_serialization=True
)

def apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt"):
    conversation = ""
    for message in messages:
        if message["role"] == "system":
            conversation += f"<s>[INST] {message['content']} [/INST]\n"
        elif message["role"] == "user":
            conversation += f"<s>[INST] {message['content']} [/INST]\n"
        elif message["role"] == "assistant":
            conversation += f"<s>[INST] {message['content']} [/INST]\n"
    if add_generation_prompt:
        conversation += "<s>[INST]"
    inputs = tokenizer(conversation, return_tensors=return_tensors, padding=True)
    return inputs

@app.route('/model', methods=['POST'])
def model_endpoint():
    keyword_url = "http://127.0.0.1:5000/" 
    headers = {'Content-Type': 'application/json'}
    req_data = request.get_json()

    keyword_response = requests.post(keyword_url, headers=headers, json=req_data).json()
    text = keyword_response['template']['outputs'][0]['simpleText']['text']
    text_out = req_data['userRequest']['utterance']

    # 대화형 메시지 설정
    messages = [
        {"role": "system", "content": "모든 대답은 한국어(Korean)으로 대답해줘. 너는 법률상담 전문가야. user의 질문은 assistant가 주는 정보를 이용해서 법률 답변을 생성하자."},
        {"role": "user", "content": text},
        {"role": "assistant", "content": text_out}
    ]
    
    inputs = apply_chat_template(messages).to(model.device)

    terminators = [tokenizer.eos_token_id]

    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=1024,
        min_length=50,
        eos_token_id=terminators[0],
        do_sample=False,  # 샘플링 대신 확정적인 응답을 생성
        temperature=1.0,  # 그리디 디코딩설정
        repetition_penalty=1.2,  # 반복 억제 페널티 설정
    )

    response_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                }
            ]
        }
    }

    return jsonify(res)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
