import os
from langchain_community.vectorstores import FAISS#FAISS向量数据库
from langchain_huggingface import HuggingFaceEmbeddings#huggingfasce文本->向量
_embeddings=HuggingFaceEmbeddings(
model_name="E:/ai-app-prep/day3/emb_model",#多语言向量模型
    encode_kwargs={"normalize_embeddings": True},#归一化向量
)
_vector_store=None
def get_vector_store():
    global _vector_store
    if _vector_store is None:#判断是否有已保存索引
        if os.path.exists('./faiss_index'):
            _vector_store=FAISS.load_local(#本地加载已保存索引
                './faiss_index',#本地路径
                _embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            _vector_store=FAISS.from_texts(["初始化"],_embeddings)#新建向量库，塞入假文本占位
    return _vector_store
def add_documents(chunks):
    vs=get_vector_store()#获取全局向量库
    vs.add_documents(chunks)#追加保存文档
    vs.save_local(#保存到硬盘
        './faiss_index', )
def search(query:str,k:int=3):
    query_text = f"为这个句子生成表示以用于检索相关文章：{query}"
    vs=get_vector_store()
    results=vs.similarity_search_with_score(query_text, k=k)#返回相似度最高的k条chunk默认为3
    return results
