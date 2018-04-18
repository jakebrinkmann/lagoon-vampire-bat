FROM continuumio/miniconda3:4.4.10

RUN conda config --add channels conda-forge \
    && conda install -yq gdal

COPY . /usr/local/src
WORKDIR /usr/local/src

RUN pip install --no-cache-dir -e .
