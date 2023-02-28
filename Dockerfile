FROM python:3
#tworzą zmienne środowiskowe:
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /code
#COPY requirements.txt /code/

#RUN pip install --upgrade pip \
#RUN pip install Django
#RUN pip install pillow
#RUN pip install psycopg2-binary
#RUN pip install sorl-thumbnail
#RUN pip install dal


RUN python3 -m venv /venv

#echo venv/ >> .gitignore \
# source venv/bin/activate
#echo Django >> requirements.txt \
#echo pillow >> requirements.txt \
#echo psycopg2-binary >> requirements.txt \
#echo sorl-thumbnail >> requirements.txt \
#echo dal >> requirements.txt
COPY requirements.txt .
#pip install --upgrade pip
RUN . /venv/bin/activate && pip install -r requirements.txt


COPY . /code/

#EXPOSE 8000
#
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "arma.wsgi:application"]