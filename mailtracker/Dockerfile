FROM python:3.8-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

COPY ./app /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8050

CMD ["python", "/app/application.py"]