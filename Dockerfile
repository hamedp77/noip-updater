FROM python:slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY no_ip.py exceptions.py ./

CMD [ "python", "./no_ip.py" ]
