from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi
import jieba
from day3.vector_store import get_vector_store
class HybridSearch:
    def __init__(self,bm25_weight=0.3,vector_weight=0.7):#权重0.3:0.7
        self.bm25_weight=bm25_weight
        self.vector_weight=vector_weight
        self.bm25=None#标记未构建索引
        self.bm25_docs=[]#村全部文档原文
        self.doc_metadata=[]#文档对应的元数据(来源,ID,标题.......
    def rebuild(self):
        from .store import ALL_CHUNKS
        if not ALL_CHUNKS:
            return
        self.bm25_docs = [d.page_content for d in ALL_CHUNKS]
        self.doc_metadata = [d.metadata for d in ALL_CHUNKS]
        tokenized=[list(jieba.cut(d.page_content)) for d in ALL_CHUNKS]
        self.bm25=BM25Okapi(tokenized)
        from day3.vector_store import _embeddings
        self.faiss=FAISS.from_documents(ALL_CHUNKS,_embeddings)

    def build_index(self,documents:list[dict]):#构建BM25索引
        self.bm25_docs=[d["content"] for d in documents]
        self.doc_metadata=[d["metadata"] for d in documents]
        #入参格式documents = [
        #{"content":"RAG由检索+生成组成", "metadata":{"id":1,"title":"RAG介绍"}},
        #{"content":"BM25是关键词检索算法", "metadata":{"id":2,"title":"BM25原理"}}
        #]
        tokenized=[list(jieba.cut(doc))for doc in self.bm25_docs]#jieba.cut(doc)中文分词
        self.bm25=BM25Okapi(tokenized)#分词文档给BM25构建倒排索引
    def search(self,query:str,k:int=5):#检索主函数 用户问题 返回检索条数
        if self.bm25 is None:
            #bm25未构建时退化只用向量
            vs =get_vector_store()
            results=vs.similarity_search_with_score(query,k=k)
            return [(doc.page_content,doc.metadata,score) for doc,score in results]
        query_token=list(jieba.cut(query))#对query分词
        bm25_scores=self.bm25.get_scores(query_token)#返回每一篇文档的BM25原始分
        vs=get_vector_store()#向量检索
        vector_results=vs.similarity_search_with_score(query,k=len(bm25_scores))#拿到所有的文档向量数据
        vector_score_map={doc.page_content:score for doc,score in vector_results}#字典映射
        combined=[]
        for i,content in enumerate(self.bm25_docs):#分数归一化 加权融合
            bm25_norm=bm25_scores[i]/(max(bm25_scores)+1e-8)#缩放到0-1
            vector_score=vector_score_map.get(content,1.0)#寻找不到给最低1.0
            vector_norm=1-(vector_score/(max(vector_score_map.values())+1e-8))#距离分
            fused=self.bm25_weight*bm25_norm + self.vector_weight*vector_norm#融合分数
            combined.append((content,self.doc_metadata[i],fused))
        combined.sort(key=lambda x:x[2],reverse=True)
        return combined[:k]#返回按融合分从高到低取前k条
hybrid_search=HybridSearch()
#优化方向 检索文档从全部减少到前top20
#依靠page_content做key匹配改为入库时带上唯一id映射分数
#用min-max归一化避免最高分被带偏
#做切片去重