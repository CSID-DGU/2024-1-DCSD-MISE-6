from openai import OpenAI



def create_output(text):

    client = OpenAI(api_key='key')

    completion = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-1106:personal:final5:9S6zzH2V", # model id 추가
    messages=[
        {"role": "system", "content": "You are a legal expert who must explain as quickly and concisely as possible."},
        {"role": "user", "content": text}
    ]
    )
    return completion.choices[0].message.content