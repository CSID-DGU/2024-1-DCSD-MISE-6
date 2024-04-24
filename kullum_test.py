from transformers import AutoModel, AutoTokenizer

# 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("nlpai-lab/kullm-polyglot-5.8b-v2")
model = AutoModel.from_pretrained("nlpai-lab/kullm-polyglot-5.8b-v2")

# 입력 텍스트
text = ""

# 토크나이징 및 입력 형식 준비
inputs = tokenizer(text, return_tensors="pt")

# 모델에 입력 데이터 전달
outputs = model(**inputs)

# 마지막 은닉 상태 추출
last_hidden_states = outputs.last_hidden_state

# 결과 사용 예
print(last_hidden_states.shape)
