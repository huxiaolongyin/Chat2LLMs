#!/bin/bash
# phoenix
python3 -m phoenix.server.main serve &
# fast_api
uvicorn src.main:app --host 0.0.0.0  --port 8000 &
# streamlit
streamlit run src/streamlit_app/main.py