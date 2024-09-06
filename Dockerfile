FROM python:3.8-slim

WORKDIR /code

COPY ./pyproject.toml ./code

COPY ./src ./code/src

# 移动虚拟环境
COPY ./.venv ./code/.venv

ENV PATH="/code/.venv/Scripts:$PATH"

RUN python -m pip install .


EXPOSE 8000

CMD unicorn src.fastapi_app:app \
    --host 0.0.0.0 \
    --port 8000 \