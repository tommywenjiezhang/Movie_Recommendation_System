FROM tiangolo/uwsgi-nginx-flask:python3.6

WORKDIR /app/

COPY requirements.txt /app/
RUN pip3 install -r ./requirements.txt

ENV ENVIRONMENT production


COPY . /app

EXPOSE 5555


# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["main.py" ]