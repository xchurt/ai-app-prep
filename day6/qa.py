import os
from langchain_core.messages import HumanMessage, AIMessage
from openai import AsyncOpenAI
from .session_store import get_or_create_session,add_message,get_history
from day4.hybird_search import hybrid_search
async def chat_with_history(session_id:str,question:str):#id会话标识绑定上下文 q当前提问
    client=AsyncOpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
    )
    results=hybrid_search.search(question,k=3)#混合搜索（不带历史
    context_parts=[]#拿到原文片段提示给大模型
    sources=[]#记录来源文档+相似度得分
    for content,metadata,score in results:
        context_parts.append(content)
        source=metadata.get("source","未知")
        sources.append(f"{source}(得分:{score:.3f})")
    context=("\n---\n".join(context_parts) if context_parts else "无相关文档")
    sid,_=get_or_create_session(session_id)#获取对话历史
    history=get_history(sid)
    messages=[]#构建消息列表
    messages.append({#系统提示
        "role": "system",
        "content": f"""你是企业知识库助手。根据参考资料回答用户问题。
如果参考资料中找不到答案，请明确说"资料中未提及"。
回答要简洁准确，引用相关制度条款。

参考资料：
{context}"""
    })
    for msg in history:#历史消息
        if isinstance(msg,HumanMessage):
            messages.append({"role":"user","content":msg.content})
        elif isinstance(msg,AIMessage):
            messages.append({"role":"assistant","content":msg.content})
    messages.append({"role":"user","content":context})#当前问题
    resp=await client.chat.completions.create(#异步请求AI对话
        model=os.getenv("MODEL_NAME","deepseek-chat"),
        messages=messages,
        temperature=0.3
    )
    answer=resp.choices[0].message.content
    add_message(sid,"user",question)#保存历史
    add_message(sid,"assistant",answer)
    return {
        "answer":answer,#模型回答
        "session_id":sid,
        "sources":list(set(sources)),#去重后的知识库来源
        "context_used":context_parts,#本次检索片段
        "history_length":len(history)+2#总消息条数
    }