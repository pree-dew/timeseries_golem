from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ts_golem",
    version='0.1',
    install_requires=required,
    entry_points='''
        [console_scripts]
        ts_golem_validate=ts_golem.interface:validate_schema
        ts_golem_generate=ts_golem.interface:generate_signal
    ''',
)
