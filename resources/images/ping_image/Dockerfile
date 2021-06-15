# Pull base image of latest Python 3.7.x
FROM python:3.7-alpine

RUN apk update
RUN apk add curl
RUN apk add iputils
RUN apk add iperf

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD run_pings.py /code/
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "run_pings.py"]