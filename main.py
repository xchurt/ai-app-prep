from idlelib.pathbrowser import PathBrowser
from fastapi import FastAPI,UploadFile,File
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()#加载根目录的env
app=FastAPI(title="AI App Prep")
Path("./data").mkdir(exist_ok=True)
from day2.main import router as day2_router
app.include_router(day2_router,prefix="/day2")
from day3.qa import rag_answer
from day3.loader import load_and_split
from day3.vector_store import add_documents
@app.post("/day3/rag/upload")
async def upload_doc(file: UploadFile = File(...)):
    file_path=f"./data/{file.filename}"
    with open(file_path,"wb") as f:
        f.write(await file.read())
    chunks=load_and_split(file_path)
    add_documents(chunks)
    return {"ok":True,"chunks":len(chunks)}
@app.post("/day3/rag/ask")
async def rag_ask(question:str):
    return await rag_answer(question)
@app.get("/")
async def root():
    return {"status":"ok","days":["day1","day2","day3"]}
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000,reload=True)
