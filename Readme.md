**timeseries_golem** is designed to emit the signal as per the given instruction, just like a golem.
It is useful when:
1. Specific signal patterns are required to test timeseries use cases like alerting, anomaly etc.
2. Specific types of distribution are required to test its behaviour.
3. Opentelemetry output needs to be tested against any backend at scale.


**Instructions to run golem**

Installation and setup:

`make setup`


**To validate signal configuration:**

`ts_golem validate -sg signal_details.json`


**To generate timeseries:**

`ts_golem generate -sg signal_details.json -cf exporter_config.json`


**To generate timeseries with hot reload for signal_details json:**

`ts_golem generate -sg signal_details.json -cf exporter_config.json --reload`
