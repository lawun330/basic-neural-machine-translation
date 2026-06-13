# Burmese G2P web UI + Marian inference (HF Space / local Docker)
#
# build from repo root:
#   docker build -f docker/Dockerfile -t basic-neural-machine-translation .
#
# run:
#   docker run -p 7860:7860 \
#     -e HF_MODEL_REPO=lawun330/basic-neural-machine-translation \
#     -e HF_TOKEN=hf_xxx \
#     -e MARIAN_DECODER=/usr/local/bin/marian-decoder \
#     -e HOST=0.0.0.0 \
#     basic-neural-machine-translation

FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
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
