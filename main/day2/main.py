from dotenv import load_dotenv
from fastapi import FastAPI
from openai.types.beta.chatkit import ChatKitResponseOutputText
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
app=FastAPI(title="Day2")#实例化应用
client=AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)
class ChatReq(BaseModel):#基础请求体模型
    message:str
@app.get("/")#检查接口是否正常
async def root():
    return {"status":"ok"}
@app.post("/chat")
async def chat(req:ChatReq):#普通非流式对话
    resp=await client.chat.completions.create(#异步的调用大模型接口
        model=os.getenv("MODEL_NAME","deepseek-chat"),
        messages=[{"role":"user","content":req.message}],#传入当前用户信息
        temperature=0.7,#控制随机性
    )
    return{"reply":resp.choices[0].message.content,"model":os.getenv("MODEL_NAME"),"usage":resp.usage.model_dump() if resp.usage else None}
from fastapi.responses import StreamingResponse
@app.post("/chat/stream")
async def chat_stream(req:ChatReq):
    async def generate():
        stream = await client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "deepseek-chat"),
            messages=[{"role": "user", "content": req.message}],
            stream=True,#流式返回开启
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:#流式返回增量文本 类似普通接口的message.content
                yield chunk.choices[0].delta.content
    return StreamingResponse(generate(),media_type="text/plain")#generate异步生成器
class ChatReqV2(BaseModel):
    message:str
    system_prompt:str="你是一个专业的AI应用开发助手,回答简洁有力"#系统角色设定
    history:list[dict]=[]#历史对话数组
@app.post("/char/v2")
async def chat_v2(req:ChatReqV2):
    messages=[{"role":"system","content":req.system_prompt}]
    messages.extend(req.history)
    messages.append({"role":"user","content":req.message})
    resp= await client.chat.completions.create(model=os.getenv("MODEL_NAME","deepseek-chat"),messages=messages,temperature=0.7)
    return {"reply":resp.choices[0].message.content}
if __name__=="__main__":#服务器启动
    import uvicorn
    uvicorn.run("main:app",port=8000,reload=True)