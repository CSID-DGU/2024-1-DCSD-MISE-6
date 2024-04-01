import pandas as pd
import json
from data_preprocessing import *

if __name__ == '__main__':
    df1 = read_jsonl('law_qa_dataset.jsonl')
    df2 = read_jsonl('Lawsee_ko_QA.jsonl')
    df3 = read_jsonl('preference.jsonl')
    df4 = pd.read_json('생활법령.json')
    df5 = read_jsonl('legalqa.jsonlines.txt')

    df1 = df1.drop('precedent',axis=1)
    df2 = df2.drop('precedent',axis=1)
    df3 = df3.drop('rejected',axis=1)
    df5 = df5.drop(['title','id'],axis=1)
    df3 = df3.rename(columns={'prompt': 'question','chosen':'answer'})
    df4 = df4.rename(columns={'instruction': 'question','output':'answer'})


    df_total = pd.concat([df1, df2, df3,df4,df5])
    df_total = df_total.drop('input',axis=1)
    df_total.to_csv('df_total.csv', index=False, encoding='utf-8-sig')

    preprocessed_df = df_total.assign(instruction=df_total["question"].apply(preprocess), output=df_total["answer"].apply(preprocess))
    df_total = preprocessed_df


    sentence = ['안녕하세요. 귀하께서 질의하신 내용은 저의 전문분야가 아니므로 번거로우시더라도 다른 전문분야 전문인에게 다시 한번 질의하시기 바랍니다.',
            '상담자님이 문의해 주신 상담글에 대해 답변이 어려운점 양해 말씀드립니다.']
    df_total = remove_rows_with_strings(df_total, 'answer', sentence)
    df_total.to_csv('data_filter.csv', index=False, encoding='utf-8-sig')
