import streamlit as st
from pathlib import Path
from safetensors.flax import save_file
from api_client import upload_doc,ask_question
from api_client import BASE_URL
print("API BASE_URL:", BASE_URL)
st.set_page_config(page_title="RAG知识库问答",page_icon="📚",layout="wide")#页面全局配置
st.title("📚RAG知识库问答Demon")
with st.sidebar:#左边侧边栏，文件选择框，只允许txt,md
    st.header("📁文档管理")
    uploaded_file=st.file_uploader("上传知识文档",type=["txt","md"])
    if uploaded_file is not None:
        save_path=f"./data/{uploaded_file.name}"
        Path("./data").mkdir(exist_ok=True)#没有data就新建
        with open(save_path,"wb") as f:
            f.write(uploaded_file.getbuffer())#拿到上传的二进制文件写入本地磁盘
        if st.button("📤上传到知识库",type="primary"):
            with st.spinner("上传中..."):#转圈加载动画
                result=upload_doc(save_path)
            if result.get("ok"):
                st.success(f"上传成功!共{result.get('chunks','?')}个片段")
            else:
                st.error(f"上传失败:{result}")
    st.divider()
    st.caption("后端:FastAPI+BGE+FAISS+BM25")
    st.caption("前端:Streamlit")
st.header("💬提问")
if "messages" not in st.session_state:#初始化聊天历史
    st.session_state.messages=[]#浏览器会话内存
for msg in st.session_state.messages:
    st.write(msg["content"])
    if "sources" in msg:
        with st.expander("来源"):
            for s in msg["sources"]:
                st.caption(s)
question=st.chat_input("输入你的问题...")
if question:
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("检索中..."):
            result=ask_question(question)
        answer=result.get("answer","出错了")
        st.write(answer)
        sources=result.get("sources",[])
        if sources:
            with st.expander("检索来源"):
                for s in sources:
                    st.caption(s)
        context_used=result.get("context_used",[])
        if context_used:
            with st.expander("召回的上下文"):
                for i,ctx in enumerate(context_used):
                    st.text_area(f"片段{i+1}",ctx,height=100)
    st.session_state.messages.append({
        "role":"assistant",
        "content":answer,
        "sources":sources,
        "context_used":context_used
    })
#网页上传txt/md传入本地./data/->点按钮调用upload_doc发给FastAPI存入向量库->聊天框提问ask_question请求后端->返回回答来源召回片段，页面渲染聊天记录
