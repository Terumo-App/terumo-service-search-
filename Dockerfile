FROM python:3.10.11-slim
# FROM python:3.10.11-slim-bullseye

RUN mkdir /src
RUN mkdir /src/db

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /src/ /src/


CMD ["python", "app.py", "--reload=False"]