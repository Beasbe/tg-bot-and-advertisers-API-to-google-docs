
FROM python:3.9-slim

WORKDIR /GetStat


COPY . /GetStat

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "bootstrap.py"]