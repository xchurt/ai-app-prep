from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def load_and_split(file_path:str,chunk_size:int=300,chunk_overlap:int=50):#路径 最长字符 重叠字符
    if file_path.endswith('.pdf'):
        loader=PyPDFLoader(file_path)
    else:
        loader=TextLoader(file_path,encoding="utf-8")
    documents=loader.load()
    splitter=RecursiveCharacterTextSplitter(#分割器
        chunk_overlap=chunk_overlap,
        chunk_size=chunk_size,
        separators=["\n\n","\n","。","!","？","："," ",""]#分割字符
    )
    chunks=splitter.split_documents(documents)
    return chunks
#流程 文件>loader_load>document的全部文件>recursivecharactertextsplitter>小段文本>向量化>存入FAISS