FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY responder.py .
USER 10001
EXPOSE 8081
CMD ["uvicorn", "responder:app", "--host", "0.0.0.0", "--port", "8081"]
