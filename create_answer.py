from openai import OpenAI



def create_output(text):

    client = OpenAI(api_key='key')

    completion = client.chat.completions.create(
    model="fine-tuning model",
    messages=[
        {"role": "system", "content": "You are a legal expert who must explain as quickly and concisely as possible."},
        {"role": "user", "content": text}
    ]
    )
    return completion.choices[0].message.content