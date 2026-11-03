from .vector_store import search
from openai import AsyncOpenAI
import os
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
if not api_key or not base_url:
    raise ValueError("API_KEY 或 BASE_URL 未配置，请检查 .env")
client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url)
async def rag_answer(question:str):
    results=search(question,k=3)#检索
    context_parts=[]#拼接上下文
    sources=[]
    for doc,score in results:
        context_parts.append(doc.page_content)#切片后文本内容
        source=doc.metadata.get("source","未知")#文档名信息
        sources.append(f"{source}(相关度:{score:.2f})")
    context="/n---/n".join(context_parts)
    prompt=f"""根据以下参考资料回答问题。如果参考资料中找不到答案，请明确说"资料中未提及"。
参考资料：
{context}

问题：{question}

回答："""#拼接索引成参考资料喂给大模型
    resp=await client.chat.completions.create(
        model=os.getenv("MODEL_NAME","deepseek-chat"),
        messages=[{"role":"user","content":prompt}],
        temperature=0.3,
    )#await异步等待
    results = search(question, k=3)
    print("检索到的上下文：", [doc.page_content for doc, _ in results])
    return {
        "answer":resp.choices[0].message.content,#模型回复
        "sources":list(set(sources)),#同一文件检索去重
        "context_used":context_parts,#给前端看模型看到的原文
    }
#流程 用户提问>rag_answer>search检索拿到相似chunk>拼接>塞入prompt防止幻觉>异步请求LLM>返回