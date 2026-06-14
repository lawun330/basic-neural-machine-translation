# Basic Neural Machine Translation - Web UI + Marian inference (Local)
#
# prerequisite: create .env with environment variables
# - HF_MODEL_REPO
# - HF_TOKEN
#
# build from repo root:
#   docker build -f docker/Dockerfile -t basic-nmt .
#
# run:
#   docker run -p 7860:7860 --env-file .env basic-nmt

FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY syl-normalizer/ /app/syl-normalizer/
COPY data/vocab/ /app/data/vocab/
COPY web/ /app/web/

COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY docker/marian-decoder /usr/local/bin/marian-decoder
RUN chmod +x /usr/local/bin/marian-decoder

ENV PORT=7860
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV MARIAN_DECODER=/usr/local/bin/marian-decoder
ENV HF_MODEL_HUB_LAYOUT=flat

EXPOSE 7860

ENTRYPOINT ["/app/entrypoint.sh"]
