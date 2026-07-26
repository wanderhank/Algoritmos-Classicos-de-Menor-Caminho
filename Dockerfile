FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# O projeto usa apenas a biblioteca padrão do Python.
COPY . .

# Mantém o diretório de saída disponível e executa como usuário não root.
RUN mkdir -p /app/resultados \
    && useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "main.py"]
