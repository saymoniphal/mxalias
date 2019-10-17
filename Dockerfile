FROM python:3.7

RUN mkdir /mxaliases
WORKDIR /mxaliases
ADD . /mxaliases
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/mxaliases/run.py"]
