FROM continuumio/miniconda3:4.4.10

COPY . /usr/local/src
WORKDIR /usr/local/src

RUN conda config --add channels conda-forge \
    && conda install -yq gdal \
    && pip install --no-cache-dir -e .
