# Timeseries Golem

Timeseries Golem is a Python library designed to emit metric signals as per the given instruction, just like a golem.

It is useful when:
1. Specific signal patterns are required to test time-series use cases like alerting, anomaly, etc.
2. Specific types of distribution are required to test its behavior.
3. Opentelemetry output needs to be tested against any backend at scale.

It emits metrics to a remote write location such as [Levitate](https://last9.io/levitate-tsdb) using [Prometheus Remote Write](https://last9.io/blog/what-is-prometheus-remote-write/).


## Prerequisites
Install the Snappy C Library with the following commands

**DEB-based**
`$ sudo apt-get install libsnappy-dev`

**RPM-based** `$ sudo yum install csnappy-devel`

**Alpine (Docker)** `RUN apk add --no-cache snappy-dev g++`

**openSUSE** `$ sudo zypper in snappy-devel`

**MacOS Intel** 
```shell
$ brew install snappy
$ CPPFLAGS="-I/usr/local/include -L/usr/local/lib" pip install python-snappy
```

**MacOS Apple Silicon**
```shell
$ brew install snappy
$ CPPFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" pip install python-snappy
```

## Installation

```shell
$ make setup
```
### Usage

```shell
$ docker build -t ts_golem .
$ docker run ts_golem <commands_as_per_below_use_cases>
```

## Use Cases
**To validate signal configuration:**

```shell
$ docker run ts_golem ts_golem validate -sg signal_details.json
```
**To generate time series:**
```shell
$ docker run ts_golem ts_golem generate -sg signal_details.json -cf exporter_config.json
```
**To generate time series with hot reload for signal_details json:**
```shell
$ docker run ts_golem ts_golem generate -sg signal_details.json -cf exporter_config.json --reload
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

