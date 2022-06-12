FROM python:3.9

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

# RUN apt update
# && apt install build-base
#  && add python3-dev libpq-dev && apk add build-base


RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . ./app
RUN cd /app 

CMD ["python3", "/app/main.py"]