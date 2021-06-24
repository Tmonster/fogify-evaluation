# Pull base image of latest Python 3.7.x
FROM python:3.7-alpine

RUN apk update
RUN apk add curl
RUN apk add iputils
RUN apk add iperf3

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD bandwidth_src /code/bandwidth_src
ADD ping_src /code/ping_src
ADD utils /code/utils
ADD main.py /code/
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "main.py"]