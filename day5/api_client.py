import requests
BASE_URL="http://127.0.0.1:8000"#后端服务地址常量
def upload_doc(file_path:str):#上传txt知识库文档给本地RAG存入向量库
    with open(file_path, 'rb') as f:#with自动关闭文件 只读文件
        files={"file": (file_path.split("/")[-1], f,"text/plain")}#后端接口接收文件参数名 "text/plain"MIME纯文本
        resp=requests.post(f"{BASE_URL}/day4/upload",files=files)#发送POST请求 访问上传接口
        return resp.json()#后端返回JSON转为字典返回
def ask_question(question:str):#问题发给后端，拿到回答后返回
    resp=requests.post(f"{BASE_URL}/day4/ask",json={"question":question})#POST请求 把query参数传给day4/ask/
    return resp.json()