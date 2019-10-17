FROM python:3.7

LABEL maintainer "Kushal&Moniphal [mxaliases@locationd.net]"

RUN mkdir /mxaliases
WORKDIR /mxaliases
ADD . /mxaliases
RUN pip install -r requirements.txt

EXPOSE 6008 
CMD ["python", "/mxaliases/run.py"]
