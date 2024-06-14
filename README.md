# 2024-1-DCSD-MISE-6

## 프로젝트 소개
<span style="font-size: 20px;"><b>오픈 소스 기반 법률 상담 챗봇</b></span>


<h2>팀 구성</h2>

|                   팀장                    |                     팀원                     |                              팀원                               |                               팀원                                |
| :-----------------------------------------: | :--------------------------------------------: | :-------------------------------------------------------------: | :-------------------------------------------------------------: |
| ![](https://github.com/lee-cheolwoo.png?size=100) | ![](https://github.com/seonggeuns.png?size=100) | <img src="https://github.com/y8jinn.png" width="400px" height="150px"/> | <img src="https://github.com/JianKim3293.png?size=100"> |
|     [이철우](https://github.com/lee-cheolwoo)     |     [최성근](https://github.com/seonggeuns)     |           [정유진](https://github.com/y8jinn)            |           [김지안](https://github.com/JianKim3293)            |

## 개발 목표

- 사용자 맞춤형 실시간 법률 상담 제공
- 법률 서비스 접근성 개선
- 시간적, 경제적 제약 없이 법률 조언 제공
- 법적 권리 보호 및 법률적 분쟁 예방

## 최종 결과 설명

카카오톡 채널을 통해 구현된 법률 상담 챗봇입니다. 사용자는 법률 관련 이미지나 텍스트를 통해 챗봇에게 질문할 수 있고, 챗봇은 이를 분석하여 적절한 답변을 제공합니다.

이 프로젝트를 실행하기 위해 필요한 패키지는 다음과 같습니다:
- `numpy==1.22.4`
- `pandas==2.0.3`
- `scipy==1.10.1`
- `matplotlib-inline==0.1.7`
- `tensorflow==2.8.2`
- `torch==2.2.2`
- `transformers==4.37.2`
- `flask==3.0.3`
- `requests==2.22.0`
- `google-cloud-vision==3.0.2`
- `peft==0.8.2`

설치하려면 다음 명령어를 사용하세요:
```sh
pip install -r requirements.txt