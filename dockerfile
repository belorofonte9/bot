FROM python:3.8

LABEL Maintainer="gsampallo"

WORKDIR /usr/app/src

COPY *.py ./
COPY requirements.txt ./
COPY chromedriver ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./bot_selenium.py"]