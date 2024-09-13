FROM bitnami/pytorch:1.13.0

WORKDIR /code

COPY ./pyproject.toml .

COPY ./README.md .

COPY ./src ./src

USER root
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install --upgrade pip setuptools wheel 
RUN pip3 install .

COPY ./start.sh .

EXPOSE 8000 6006 8501

RUN chmod +x /code/start.sh

CMD ["/code/start.sh"]