FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY sale_app.py ./

RUN pip install --no-cache-dir requests

CMD ["python", "sale_app.py"]
