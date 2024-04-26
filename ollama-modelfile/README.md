## HuggingFace gguf 파일을 Ollama 로딩

> HuggingFace-Hub 설치
```bash
pip install huggingface-hub
```

아래의 예시는 `nlpai-lab/KULLM3`
- GGUF: https://huggingface.co/javiagu/KULLM3-GGUF

GGUF 파일을 다운로드 받기 위하여 https://huggingface.co/javiagu/KULLM3-GGUF 에서 원하는 .gguf 모델을 다운로드 받습니다.

순서대로
- `HuggingFace Repo`
- .gguf 파일명
- local-dir 설정
- 심볼릭 링크 설정
  
```bash
huggingface-cli download \
  javiagu/KULLM3-GGUF \
  kullm3.Q8_0.gguf \
  --local-dir 본인의_컴퓨터_다운로드폴더_경로 \
  --local-dir-use-symlinks False
```

### Modelfile

> nlpai-lab/KULLM3
```
FROM kullm3.Q8_0.gguf

TEMPLATE """{{- if .System }}
<s>{{ .System }}</s>
{{- end }}
<s>Human:
{{ .Prompt }}</s>
<s>Assistant:
"""

SYSTEM """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."""

PARAMETER stop <s>
PARAMETER stop </s>
```


```

## Ollama 실행

```bash
ollama create kullm3.Q8_0 -f kullm3.Q8_0.gguf/Modelfile
```

Ollama 모델 목록

```bash
ollama list
```

Ollama 모델 실행

```bash
ollama run kullm3.Q8_0:latest
```

## LangServe 에서 Ollama 체인 생성

app 폴더 진입 후

```bash
python server.py
```

## ngrok 에서 터널링(포트 포워드)

```bash
ngrok http localhost:8000
```
![](./images/capture-20240411-035817.png)

NGROK 도메인 등록 링크: https://dashboard.ngrok.com/cloud-edge/domains

> 고정 도메인이 있는 경우
```bash
ngrok http --domain=poodle-deep-marmot.ngrok-free.app 8000
```

## GPU 사용량 모니터링

Github Repo: https://github.com/tlkh/asitop

```bash
pip install asitop
```

패스워드 설정
```bash
sudo asitop
```
실행
```bash
asitop
```

## License

본 코드는 테디노트의 코드를 참고하였음.
