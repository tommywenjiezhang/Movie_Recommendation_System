FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate the environment, and make sure it's activated:
RUN conda activate recommender_system

# copy every content from the local file to the image
COPY . /app

EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["main.py" ]