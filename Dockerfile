FROM python:3
#tworzą zmienne środowiskowe:
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /code
#WORKDIR /.
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/