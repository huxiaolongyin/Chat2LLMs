#!/bin/bash
python3 -m phoenix.server.main serve &
uvicorn src.main:app --host 0.0.0.0  --port 8000 &
streamlit run src/ChatBot.py