from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ts_golem",
    version='0.1',
    install_requires=required,
    entry_points='''
        [console_scripts]
        ts_golem=ts_golem.interface:main
    ''',
)
