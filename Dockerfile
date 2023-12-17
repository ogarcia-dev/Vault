FROM python:3.11.4-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /cephalopodus/vault

COPY ./requirements.txt /cephalopodus/vault/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /cephalopodus/vault/requirements.txt

COPY ./src /cephalopodus/vault

CMD ["python3", "-u", "main.py"]