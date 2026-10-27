FROM python:3.12-slim-bookworm

# Trae uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:0.10.11 /uv /bin/

WORKDIR /app

# Instala las dependencias primero para aprovechar la caché de capas
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Copia el código y usa el entorno virtual creado por uv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Se arranca como paquete (app.main) porque main.py usa imports relativos
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
