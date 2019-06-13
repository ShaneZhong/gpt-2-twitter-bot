# this dockerfile is used for tweepy only.
FROM python:3.7.3-stretch

# install crontab and text editor
RUN apt-get update && apt-get -y install cron
RUN apt-get -y install vim

# copy files
RUN mkdir /gpt-2
WORKDIR /gpt-2
ADD . /gpt-2

# install dependencies
RUN pip3 install -r requirements_tweepy.txt

CMD ["tail", "-f", "/dev/null"]