FROM registry.cn-zhangjiakou.aliyuncs.com/publicci/python:3.12.10-slim-bookworm-make

COPY . /workspace/src

WORKDIR /workspace/src

RUN uv venv .venv
RUN uv sync --frozen --no-cache

EXPOSE 11915

CMD .venv/bin/uvicorn src.main:app --port 11915 --host 0.0.0.0
