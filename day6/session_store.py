from langchain_core.messages import HumanMessage,AIMessage
from typing import List
import uuid
SESSIONS={}#内存会话存储
def get_or_create_session(session_id: str=None):#获取或创建会话
    if session_id is None:#无id自动生成
        session_id = str(uuid.uuid4())
    if session_id not in SESSIONS:#会话不存在就新建
        SESSIONS[session_id]={
            "history":[],
            "created_at":None,
        }
    return session_id,SESSIONS[session_id]#返回id+会话字典
def add_message(session_id: str,role:str,content:str):#添加消息到历史会话
    if session_id not in SESSIONS:#会话不存在直接跳过不抛出异常
        return
    if role=="user":#对会话分类
        SESSIONS[session_id]["history"].append(HumanMessage(content=content))
    else:
        SESSIONS[session_id]["history"].append(AIMessage(content=content))
def get_history(session_id: str,max_turns:int=5):
    if session_id not in SESSIONS:
        return []
    history = SESSIONS[session_id]["history"]
    return history[-(max_turns*2):]#获取最近max_turn*2条消息