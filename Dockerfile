# this dockerfile is used for tweepy only.
FROM python:3.7.3-stretch

RUN mkdir /gpt-2
WORKDIR /gpt-2
ADD . /gpt-2

RUN pip3 install -r requirements_tweepy.txt

CMD ["tail", "-f", "/dev/null"]