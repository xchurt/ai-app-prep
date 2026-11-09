from fastapi import APIRouter
from pydantic import BaseModel
from .qa import chat_with_history
router=APIRouter(prefix="/day6",tags=["day6"])#路由分组 接口路径前面都带上/day6
class ChatRequest(BaseModel):#请求体模型
    question:str
    session_id:str=None
@router.post("/chat")
async def chat(req:ChatRequest):#接收前端JSON
    result=await chat_with_history(req.session_id,req.question)
    return result
@router.get("/new_session")
async def new_session():
    from .session_store import get_or_create_session
    sid,_=get_or_create_session()
    return {"session_id":sid,"message":"新会话已创建"}
#day6流程:streamlit->fastapi /day6/chat0->chat_with_history(hybrid_search本地RAG检索，
#读取历史拼接prompt,请求远端DeepseekAPI,写入会话历史->返回:answer/session_id/sources/...