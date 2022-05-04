FROM python:3.8.0-slim

WORKDIR /app/src/

RUN apt-get update \
&& apt-get install gcc python-tk python3-tk tk-dev -y \
&& apt-get clean

COPY requirements.txt /app/
RUN pip3 install -r ./requirements.txt

ENV ENVIRONMENT production


COPY ./src /app/


EXPOSE 5555


# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["main.py" ]