FROM python:2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY . /usr/src/app
EXPOSE 9005
ENTRYPOINT ["python"]
CMD ["main.py"]
