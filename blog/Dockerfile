FROM python:3.7

RUN mkdir /blog
WORKDIR /blog
ADD . /blog
RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt
EXPOSE 80 8000 8001 5000
ENV SPIDER=/blog
