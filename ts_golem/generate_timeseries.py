import time
import sympy
import random
from typing import Optional, Iterable

from opentelemetry.metrics import Observation, CallbackOptions

from ts_golem.exporter_utils import get_meter

default_resolution = 60

class SimpleGauge:
    def __init__(self, meter, name, description=""):
        self.name = name
        self.description = description
        self.observations:list[metrics.Observation] = []
        
        def emit_observations(options: CallbackOptions) -> Iterable[Observation]:
            yield self.observations[-1]
            self.observations = [self.observations[-1]]
        
        meter.create_observable_gauge(
          name=self.name, 
          description=self.description,
          callbacks=[emit_observations])

    def add(self, value:int, attrs:Optional[dict[str,str]]):
        self.observations.append(Observation(value, attrs))

def register_metric(metric_type, metric_name, meter):
    metric = None
    match metric_type:
        case "gauge":
            metric = SimpleGauge(meter, metric_name)
        case "counter":
            metric = metric.create_counter(name=metric_name)
        case default:
            metric = meter.create_up_down_counter(name=metric_name)

    return metric

def find_function(func_name):
    func_map = {
            "step_signal": step_signal_generator,
            "min_max_signal": min_max_signal_generator,
            "polynomial_with_dynamic_range": polynomial_with_dynamic_range,
            "polynomial_with_static_range": polynomial_with_static_range
    }

    return func_map[func_name]


def generate_labels(signal_no, signal):
    series_count = signal.get("series_count", 1)
    label_count = signal.get("label_count", 0)
    default_labels = {
            "signal_no": str(signal_no),
            "signal_type": signal["signal_details"]["signal_type"]
    }

    all_labels = []
    for i in range(0, series_count):
        labels = default_labels.copy()
        labels['series_id'] = str(i)
        for l in range(0, label_count):
            labels["labels_" + str(l)] = str(l)
        all_labels.append(labels)
   
    return all_labels


def add_value_to_metric(metric, val, all_labels):
    for ts in all_labels:
        metric.add(val, ts)

def step_signal_generator(signal_no, config, signal_details):
    metric = register_metric("up_and_down_counter", signal_details["metric"], get_meter(config))
    resolution = config.get("pickup_duration", default_resolution)
    
    all_labels = generate_labels(signal_no, signal_details)
    repeat_for = signal_details["signal_details"]["repeat_for"]
    low_val = signal_details["signal_details"]["low-amplitude"]
    high_val = signal_details["signal_details"]["high-amplitude"]
    
    last_val = high_val
    while True:
        val = high_val if last_val == low_val else low_val
        for v in range(resolution, repeat_for+1, resolution):
            add_value_to_metric(metric, val, all_labels)
            time.sleep(resolution)
            if val != 0:
                last_val = val
                val = 0
        add_value_to_metric(metric, -last_val, all_labels)


def min_max_signal_generator(signal_no, config, signal_details):
    metric = register_metric("up_and_down_counter", signal_details["metric"], get_meter(config))
    resolution = config.get("pickup_duration", default_resolution)

    all_labels = generate_labels(signal_no, signal_details)
    low_val = signal_details["signal_details"]["low-amplitude"]
    high_val = signal_details["signal_details"]["high-amplitude"]
    
    last_val = high_val
    while True:
        for val in [low_val, high_val]:
            add_value_to_metric(metric, val, all_labels)
            time.sleep(resolution)
            add_value_to_metric(metric, -val, all_labels)

def generate_poly(poly, x):
    poly = sympy.polys.polytools.poly_from_expr(poly)[0]
    coeff = [int(i) for i in poly.coeffs()]
    result = coeff[0]
 
    for i in range(1, len(coeff)):
        result = result*x + coeff[i]

    return result

def polynomial_with_dynamic_range(signal_no, config, signal_details):
    metric_type = signal_details["signal_details"]["metric_type"]
    metric = register_metric(metric_type, signal_details["metric"], get_meter(config))
    resolution = config.get("pickup_duration", default_resolution)

    all_labels = generate_labels(signal_no, signal_details)
    polynomial = signal_details["signal_details"]["polynomial"]

    min_ = signal_details["signal_details"]["min"] 
    max_ = signal_details["signal_details"]["max"]
    while True:
        x=random.randint(min_, max_)
        val = generate_poly(polynomial,x)
        add_value_to_metric(metric, val, all_labels)
        time.sleep(resolution)

def polynomial_with_static_range(signal_no, config, signal_details):
    metric_type = signal_details["signal_details"]["metric_type"]
    metric = register_metric(metric_type, signal_details["metric"], get_meter(config))
    resolution = config.get("pickup_duration", default_resolution)
  
    all_labels = generate_labels(signal_no, signal_details)
    polynomial = signal_details["signal_details"]["polynomial"]

    range_ = signal_details["signal_details"]["range"]
    repeat_for = signal_details["signal_details"]["repeat_for"]
    while True:
        for x in range_:
            for v in range(resolution, repeat_for+1, resolution):
                val = generate_poly(polynomial,x)
                add_value_to_metric(metric, val, all_labels)
                time.sleep(resolution)


