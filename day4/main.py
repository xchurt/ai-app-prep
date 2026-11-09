from fastapi import APIRouter,UploadFile,File
from fastapi.responses import JSONResponse
from .qa import hybrid_qa
from .hybird_search import hybrid_search
from day3.loader import load_and_split
from pydantic import BaseModel
from day3.vector_store import add_documents
router = APIRouter(tags=["day4"])#路由分组
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path=f"./data/{file.filename}"#保存上传文件到本地
    with open(file_path,"wb") as f:
        f.write(await file.read())
    chunks=load_and_split(file_path)#加载切片
    #add_documents(chunks)#加入向量库
    #docs_for_bm25=[#同步重建BM25索引
    #    {"content":c.page_content,"metadata":c.metadata}
    #    for c in chunks
    #]
    from .store import ALL_CHUNKS
    ALL_CHUNKS.extend(chunks)
    hybrid_search.rebuild()
    return JSONResponse({
        "ok":True,
        "filename":file.filename,
        "chunks":len(chunks),
    })
class AskRequest(BaseModel):
    question: str
@router.post("/ask")
async def ask(req:AskRequest):
    result=await hybrid_qa(req.question)
    return result

