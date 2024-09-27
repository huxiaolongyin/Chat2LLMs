python -m phoenix.server.main serve
uvicorn src.main:app --reload
streamlit run ../src/streamlit_main.py