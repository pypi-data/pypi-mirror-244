FROM python:3.11

WORKDIR /app
COPY build/* .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install --upgrade pip && pip install *.whl && rm *.whl

ENTRYPOINT ["uvicorn", "syndb_api.main:app", "--host 0.0.0.0", "--port 80"]