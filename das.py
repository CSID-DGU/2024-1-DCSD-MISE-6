from langchain.embeddings import HuggingFaceEmbeddings


modelPath = "/content/drive/MyDrive/RAG/embedding"

# Create a dictionary with model configuration options, specifying to use the CPU for computations
model_kwargs = {'device':'cuda'}


# Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
encode_kwargs = {'normalize_embeddings': True}

# Initialize an instance of HuggingFaceEmbeddings with the specified parameters
embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,     # Provide the pre-trained model's path
    model_kwargs=model_kwargs, # Pass the model configuration options
    encode_kwargs=encode_kwargs) # Pass the encoding options



from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(file_path='/content/drive/MyDrive/데이터사이언스캡스톤/판례데이터셋/total_dataset.csv') # /home/mise6/mise_code/model/LLM/final_clean_legal2.csv
document = loader.load()