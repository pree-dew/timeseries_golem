# signal_schema.py is responsible for validating the yaml 

min_max_signal = {
    "type": "object",
    "required": [
        "signal_type",
        "low-amplitude",
        "high-amplitude"
    ],
    "properties": {
        "signal_type": {
            "enum": ["min_max_signal"],
            "type":"string"
        },
        "low-amplitude": {
            "type": "integer"
        },
        "high-amplitude": {
            "type": "integer"
        }
    }
}


step_signal = {
    "type": "object",
    "required": [
        "signal_type",
        "low-amplitude",
        "high-amplitude",
        "repeat_for"
    ],
    "properties": {
        "signal_type": {
            "enum": ["step_signal"],
            "type": "string"
        },
        "low-amplitude": {
            "type": "integer"
        },
        "high-amplitude": {
            "type": "integer"
        },
        "repeat_for": {
            "type": "integer"
        }
    }
}


sinusoidal_signal = {
    "type": "object",
    "required": [
        "signal_type",
        "amplitude",
        "periodicity"
    ],
    "properties": {
        "signal_type": {
            "enum": ["sinusoidal_signal"],
            "type": "string"
        },
        "amplitude": {
            "type": "integer"
        },
        "periodicity": {
            "type": "integer"
        }
    }
}


polynomial_with_static_range = {
    "type": "object",
    "required": [
            "signal_type",
            "metric_type",
            "polynomial",
            "range",
            "repeat_for"
    ],
    "properties": {
        "signal_type": {
            "enum": ["polynomial_with_static_range"],
            "type": "string"
        },
        "metric_type": {
            "enum": ["gauge"],
            "type": "string"
        },
        "polynomial" : {
            "type": "string"
        },
        "repeat_for": {
            "type": "integer"
        },
        "range": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
    }
}

polynomial_with_dynamic_range = {
    "type": "object",
    "required": [
            "signal_type",
            "metric_type",
            "polynomial",
            "min",
            "max"
    ],
    "properties": {
        "signal_type": {
            "enum": ["polynomial_with_dynamic_range"],
            "type": "string"
        },
        "metric_type": {
            "enum": ["gauge"],
            "type": "string"
        },
        "polynomial" : {
            "type": "string"
        },
        "min": {
            "type": "integer"
        },
        "max": {
            "type": "integer"
        }
    }
}

signal_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "metric": {
                "type": "string"
            },
            "series_count": {
                "type": "integer"
            },
            "label_count": {
                "type": "integer"
            },
            "signal_details": {
                "type": "object",
                "oneOf": [
                    min_max_signal,
                    step_signal,
                    sinusoidal_signal,
                    polynomial_with_dynamic_range,
                    polynomial_with_static_range,
                ]
            }
        },
        "required": [
            "signal_details",
            "metric",
        ],
    }
}
