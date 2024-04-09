from langchain.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever

def load_documents_from_csv(file_path):
    loader = CSVLoader(file_path=file_path)
    return loader.load()

def split_text_in_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter()
    return text_splitter.split_documents(docs)

def create_embeddings_model(api_key, model_name):
    embeddings_model = HuggingFaceInferenceAPIEmbeddings(
        api_key=api_key,
        model_name=model_name
    )
    return embeddings_model

def create_faiss_index_from_texts(texts, embeddings_model):
    db = FAISS.from_documents(texts, embeddings_model)
    # db.save_local('path','FAISS_DB') # DB 저장
    return db

def create_faiss_retriever(db):
    global ensemble_faiss_retriever
    faiss_retriever = db.as_retriever(search_kwargs={"k": 4})
    ensemble_faiss_retriever = db.as_retriever(search_kwargs={"k": 2})
    return faiss_retriever

def similarity_retrieval(retriever, query):
    return retriever.get_relevant_documents(query)

def ensemble_retrieval(query,texts):
    bm25_retriever = BM25Retriever.from_documents(texts)
    bm25_retriever.k = 2
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, ensemble_faiss_retriever],
                                           weights=[0.2, 0.8])
    return ensemble_retriever.get_relevant_documents(query)



if __name__ == "__main__":
    file_path = '/content/drive/MyDrive/데이터사이언스캡스톤/test_QA.csv' # dataset
    api_key = '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' # huggingface API
    model_name = "bespin-global/klue-sroberta-base-continue-learning-by-mnr" # embedding model
    query = "남편의 불륜으로 인해 이혼하고 싶어요" # user query

    docs = load_documents_from_csv(file_path)
    texts = split_text_in_documents(docs)
    embeddings_model = create_embeddings_model(api_key, model_name)
    db = create_faiss_index_from_texts(texts, embeddings_model)
    retriever = create_faiss_retriever(db)
    similarity_documents = similarity_retrieval(retriever, query)
    ensemble_documents = ensemble_retrieval(query,texts)

    print(similarity_documents)
    print("===" * 20)
    print(ensemble_documents)
