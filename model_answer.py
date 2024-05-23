import subprocess
import sys
import json

# 필요한 패키지 설치
def install_packages():
    packages = ["transformers", "accelerate", "bitsandbytes", "flask", "requests", "beautifulsoup4"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "-q"] + packages)

if __name__ == "__main__":
    install_packages()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, BitsAndBytesConfig

    # main.py에서 글로벌 변수 가져오기
    from main import before_text, text

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

    question = before_text
    messages = [
        {"role": "system", "content": "너는 AI 법률 상담가야. 모든 답변은 한국어로 진행해줘. text를 참고하여 question에 대해 정확하고 일관적인 답변을 해줘."},
        {"role": "user", "content": f'text: "{text}" \n\n{question}'}
    ]

    encodeds = tokenizer.apply_chat_template(messages, add_generation_prompt=False, return_tensors="pt").to("cuda")

    streamer = TextStreamer(tokenizer)
    output = model.generate(inputs=encodeds,
                            max_new_tokens=2046,
                            pad_token_id=tokenizer.eos_token_id,
                            repetition_penalty=1.2,  # 반복 억제 페널티 설정
                            top_p=0.9,
                            temperature=0.1,  # 낮은 온도로 더 보수적인 응답 생성
                            do_sample=False,  # 그리디 서치를 사용하여 일관된 답변 생성
                            streamer=streamer,
                            eos_token_id=[
                                tokenizer.eos_token_id,
                                tokenizer.convert_tokens_to_ids("<|eot_id|>")
                            ])

    decode_output = tokenizer.decode(output[0], skip_special_tokens=False, clean_up_tokenization_spaces=True)
    decode_output = decode_output.split('<|end_header_id|>')[3]
    
    # 카카오톡 채널 형식의 응답 생성
    kakao_response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": decode_output
                    }
                }
            ]
        }
    }

    
    print(json.dumps(kakao_response, ensure_ascii=False, indent=4))
