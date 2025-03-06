FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync
COPY . .
RUN uv pip install -e .

CMD uv run python ./src/metrics_dashboard/app.py
