FROM python:latest

RUN pip install click tqdm

WORKDIR /app

COPY . .

CMD ["python3", "directory_flattener.py"]
