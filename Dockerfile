FROM python:3.8

WORKDIR /.

ADD app.py .

COPY requirements.txt .

RUN mkdir scrapers

ADD scrapers/* scrapers/.

RUN pip install -r requirements.txt

ENV PYTHONPATH /.

CMD ["python", "app.py"]
# CMD ["ls"]