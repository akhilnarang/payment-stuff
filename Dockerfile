FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY app/ app/
COPY main.py .

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run"]
