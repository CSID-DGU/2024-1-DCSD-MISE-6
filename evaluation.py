from trulens_eval import TruChain, Tru
tru = Tru()

from langchain import hub
from trulens_eval.app import App
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import HuggingFaceEmbeddings
from trulens_eval.feedback.provider import OpenAI
from trulens_eval import Feedback
import numpy as np


# load embedding model
modelPath = "/content/drive/MyDrive/데이터사이언스캡스톤/embedding"
model_kwargs = {'device':'cpu'} # or cuda
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,
    model_kwargs=model_kwargs, 
    encode_kwargs=encode_kwargs 
)


# load vector store and retriever
vectorstore = FAISS.load_local('/content/drive/MyDrive/데이터사이언스캡스톤/', embeddings,'judicial_DB',allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()


# Create RAG
prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


rag_chain = (
    {"context": retriever , "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


#  Initialize Feedback Function
provider = OpenAI(api_key='your key')

context = App.select_context(rag_chain)

f_groundedness = (
    Feedback(provider.groundedness_measure_with_cot_reasons)
    .on(context.collect())
    .on_output()
)

f_answer_relevance = (
    Feedback(provider.relevance)
    .on_input_output()
)

f_context_relevance = (
    Feedback(provider.context_relevance_with_cot_reasons)
    .on_input()
    .on(context)
    .aggregate(np.mean))


# Instrument chain for logging with TruLens¶
tru_recorder = TruChain(rag_chain,
    app_id='Evaluation Test',
    feedbacks=[f_answer_relevance, f_context_relevance, f_groundedness])

response, tru_record = tru_recorder.with_record(rag_chain.invoke, "question")

with tru_recorder as recording:
    llm_response = rag_chain.invoke("question")


# Explore in a Dashboard¶
tru.run_dashboard()  # tru.stop_dashboard() # stop




