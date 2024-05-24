import sys
import pandas as pd
import csv
import re
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever



def process_query(query):
    csv.field_size_limit(sys.maxsize)
    loader = CSVLoader(file_path='/home/mise6/mise_code/total_dataset.csv')
    document = loader.load()

    # Create embeddings model
    embeddings_model = HuggingFaceInferenceAPIEmbeddings(
        api_key='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',
        model_name='bespin-global/klue-sroberta-base-continue-learning-by-mnr'
    )

    # Load vector database
    db = FAISS.load_local(
        '/home/mise6/mise_code/', 
        embeddings_model, 
        'judicial_DB', 
        allow_dangerous_deserialization=True
    )

    # Retrieve documents
    Semantic_retriever = db.as_retriever(search_kwargs={"k": 1}, allow_dangerous_deserialization=True)
    bm25_retriever = BM25Retriever.from_documents(document)
    bm25_retriever.k = 1
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, Semantic_retriever],
        weights=[0.2, 0.8],
        search_type="similarity"
    )

    final = ensemble_retriever.invoke(query)

    # Create prompt
    info = final[0].page_content.split('\n')
    # 사건명 = info[0].split(':')[1].strip()
    # 판시사항 = info[1].split(':')[1].strip()
    # 판결요지 = info[2].split(':')[1].strip()
    result_data = {
    "사건명": info[0].split(':')[1].strip(),
    "판시사항": info[1].split(':')[1].strip(),
    "판결요지": info[2].split(':')[1].strip()
    }
    return result_data