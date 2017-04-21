FROM python:2

#RUN apt-get update \
#    && apt-get install -y --no-install-recommends gcc and-build-dependencies \
#    && rm -rf /var/lib/apt/lists/* \
#    && pip install cryptography \
#    && apt-get purge -y --auto-remove gcc and-build-dependencies

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 9005

ENTRYPOINT ["python"]

CMD ["main.py"]
