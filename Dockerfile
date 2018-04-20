FROM continuumio/miniconda3:4.4.10

RUN conda config --add channels conda-forge \
    && conda install -yq gdal

RUN conda install -kyq pandas lxml matplotlib scikit-image scipy
COPY . /usr/local/src
WORKDIR /usr/local/src

RUN sed -i 's/qt5agg/agg/g' /opt/conda/pkgs/matplotlib-2.2.2-py36_1/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc
RUN pip install --no-cache-dir -e .
