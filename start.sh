#!/bin/bash
app="movie_recommender_app"
docker build -t ${app} .
docker run -it -p 5555:5555 \
  --name=${app} \
  -v $PWD:/app ${app}