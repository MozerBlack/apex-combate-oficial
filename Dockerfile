FROM python:3.13-slim

LABEL org.opencontainers.image.title="Apex Combate" \
      org.opencontainers.image.description="Plataforma tudo em um para o ecossistema das artes marciais" \
      org.opencontainers.image.vendor="Apex Combate"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8080 \
    APEX_DATA_DIR=/app/data

WORKDIR /app

RUN groupadd --system apex && useradd --system --gid apex --home-dir /app apex

COPY --chown=apex:apex server.py apex_db.py index.html apex-combate.html apex-sw.js manifest.webmanifest ./
COPY --chown=apex:apex assets ./assets
COPY --chown=apex:apex icons ./icons

RUN mkdir -p /app/data && chown -R apex:apex /app

USER apex

VOLUME ["/app/data"]
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8080') + '/api/health', timeout=3)" || exit 1

CMD ["python", "server.py"]
