FROM ubuntu:16.04

WORKDIR /usr/app

RUN apt-get update
RUN apt-get install --yes python3-pip

COPY ./ ./

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements_test.txt

CMD ["python3","runserver.py"]
