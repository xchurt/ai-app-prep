from fastapi import FastAPI
from pydantic import BaseModel
import time
app=FastAPI(title="Day1")
class ChatReq(BaseModel):
    message:str
@app.get("/")
async def root():
    return {"status":"ok"}
@app.post("/chat")
async def char(req:ChatReq):
    time.sleep(0.5)
    return {"reply":f"你说的是:{req.message}","model":"mock"}
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000,reload=True)