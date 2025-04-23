# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY ./backend/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001"]
EXPOSE 8000
