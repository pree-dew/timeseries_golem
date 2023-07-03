# timeseries_golem is designed to emit the signal as per the given instruction just like a golem.
# It is useful when:
# 1. Specific signal patterns are required to test timeseries usecases like alerting, anomaly etc.
# 2. Specific type of distribution are required to test it's behvaiour.
# 3. Opentelemetry output needs to be tested against any backend at scale.


# Instructions to run golem

# pip install ts_golem

# To validate signal configuration
# ts_validate -sg signal_details.json


# To generate timeseries
# ts_generate -sg signal_details.json -cf exporter_config.json
