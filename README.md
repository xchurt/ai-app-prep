# 企业知识库 RAG 问答系统
# 结构
- day1: FastAPI 基础
- day2: DeepSeek 大模型接入（流式）
- day3: RAG（BGE 嵌入 `day3/emb_model` + FAISS）
- day4: 混合检索（BM25 + 向量）
- day5: Streamlit 前端
- day6: 多轮对话（session_id 隔离）
- day7: 工程收尾
# 启动
pip install -r requirements.txt
cp .env.example .env  # 填 Key
uvicorn main:app --reload
# /docs 测试 day3/query、day6/chat
# 工程规范
- .env 不入库；day3/emb_model、faiss_index 不入库
- 本地模型(Day3) + 云端大模型(Day2) 双轨