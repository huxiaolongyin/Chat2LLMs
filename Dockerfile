FROM bitnami/pytorch:1.13.0

WORKDIR /code

COPY ./pyproject.toml .

COPY ./README.md .

COPY ./src ./src

USER root
RUN pip3 install --upgrade pip setuptools wheel -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install . -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./start.sh .

EXPOSE 8000 6006 8501

CMD ["/code/start.sh"]