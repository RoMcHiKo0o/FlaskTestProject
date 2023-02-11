FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /app

#CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["python3", "app.py"]