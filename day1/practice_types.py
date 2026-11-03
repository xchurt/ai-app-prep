from typing import TypedDict,List
from pydantic import BaseModel
from dataclasses import dataclass
class UserInfo(TypedDict):
    name: str
    age:int
class ChatRequest(BaseModel):
    message:str
    user_id:int
    history:List[str]=[]
@dataclass
class TokenUsage:
    promt_tokens:int
    completion_tokens:int
req=ChatRequest(message="你好",user_id=1)
print(req.model_dump())