FROM python:3.8 AS build-map

# create src folder
RUN mkdir -p /src/maps
RUN python -m venv /src/venv

# Make sure we use the virtualenv:
ENV PATH="/src/venv/bin:$PATH"

# copy dataset
COPY data/pinochet.csv /src/data/

# create virtual environment, which creates /src/venv
WORKDIR /src/maps

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# copy the contents of repo and specific files to assist setup
COPY build_maps.py ./

RUN python build_maps.py

FROM nginx:1.15.9 as serve-map

COPY --from=build-map /src/maps/index.html /www/data/index.html
COPY conf.d/maps.conf etc/nginx/conf.d/maps.conf

