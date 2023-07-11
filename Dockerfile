# FROM python:3.10.11-slim
FROM python:3.10.11-slim-bullseye

RUN mkdir /app
RUN mkdir /app/db

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY /src/ /app/src/


CMD ["python", "src/app.py", "--reload=False"]