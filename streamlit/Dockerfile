FROM python:3.8-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app 

RUN apt-get update
RUN apt-get -y install gcc
RUN pip3 install -r requirements.txt

COPY Acceuil.py Acceuil.py
COPY chargement_data.py chargement_data.py
COPY challenge_partie1.py challenge_partie1.py
COPY pages /app/pages
COPY data /app/data

CMD ["streamlit", "run", "Acceuil.py"]