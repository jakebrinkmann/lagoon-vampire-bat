FROM python:3.6


# --no-cache-dir
RUN apt-get update --assume-yes \
    && apt-get install gdal-bin python-gdal python3-gdal --assume-yes \
    && pip install  --trusted-host  pypi.python.org --trusted-host  pypi.org --trusted-host files.pythonhosted.org  --upgrade pip \
    && pip install  --trusted-host  pypi.python.org --trusted-host  pypi.org --trusted-host files.pythonhosted.org  matplotlib
COPY . /usr/local/src
WORKDIR /usr/local/src
RUN pip install -e .
