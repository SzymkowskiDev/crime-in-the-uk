FROM python:3.9


RUN apt update

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
