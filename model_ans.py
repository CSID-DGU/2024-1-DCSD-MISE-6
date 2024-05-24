# pip install -U -q transformers accelerate bitsandbytes
import subprocess
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import transformers
import torch

# 필요한 패키지 설치
def install_packages():
    packages = ["transformers", "accelerate", "bitsandbytes"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "-q"] + packages)

def model_answer(qestion_input:str,input_rag:str):

        
    model_id = "JianKim3293/llama3-KoEn-8B-Instruct-mergelaw"

    # 양자화 설정
    compute_dtype = torch.float16
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=False
    )

    # 토크나이저 불러오기
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token  # 패딩 토큰 설정

    # 양자화된 모델 불러오기
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=quant_config,
        device_map="auto"
    )

    text = input_rag
    question = qestion_input
    messages = [
        {"role": "system", "content": "너는 AI 법률 상담가야. 모든 답변은 한국어로 진행해줘. text로 입력받은 내용을 기반으로 question 질문에 대해 답해줘. 대신 답변을 못할거 같으면 죄송하다고 답변해."},
        {"role": "user", "content": f'text: "{text}" \n\n{question}'}
    ]

    encodeds = tokenizer.apply_chat_template(messages, add_generation_prompt=False, return_tensors="pt").to("cuda")

    streamer = TextStreamer(tokenizer)
    output = model.generate(inputs=encodeds,
                            max_new_tokens=1024,
                            pad_token_id=tokenizer.eos_token_id,
                            repetition_penalty=1.2,  # 반복 억제 페널티 설정
                            top_p=0.9,
                            streamer=streamer,
                            eos_token_id=[
                                tokenizer.eos_token_id,
                                tokenizer.convert_tokens_to_ids("<|eot_id|>")
                            ])

    decode_output = tokenizer.decode(output[0], skip_special_tokens=False, clean_up_tokenization_spaces=True)
    decode_output = decode_output.split('<|end_header_id|>')[3]
    return decode_output