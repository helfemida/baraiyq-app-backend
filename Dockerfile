FROM python:3.9

WORKDIR /app

COPY . /app

COPY requirements.txt /app

EXPOSE 8080

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
