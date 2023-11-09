FROM python:3.12.0-bullseye

RUN apt-get update && apt-get -y install libsnappy-dev

WORKDIR /app
COPY . /app/

RUN export CPPFLAGS="-I/usr/local/opt/zlib/include:$CPPFLAGS"
RUN pip3 install python-snappy
RUN pip3 install wheel
RUN python3 setup.py bdist_wheel --universal
RUN pip3 install dist/*.whl --force-reinstall
RUN rm -rf dist/
RUN rm -rf build/


CMD ["echo", "timeseries_golem is ready!"]
