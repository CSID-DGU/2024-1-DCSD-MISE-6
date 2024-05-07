from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(file_path='/content/drive/MyDrive/데이터사이언스캡스톤/판례데이터셋/total_dataset.csv') # /home/mise6/mise_code/model/LLM/final_clean_legal2.csv
document = loader.load()