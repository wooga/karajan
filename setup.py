from setuptools import setup

setup(
    name='karajan',
    version='0.0.7',
    url='https://github.com/wooga/bit.karajan',
    license='',
    packages=['karajan'],
    author='Wooga Business Intelligence Team',
    author_email='bit-admin@wooga.com',
    description='A conductor of aggregations in Apache Airflow',
    install_requires=[
        "behave",
        "pyyaml",
        "airflow>=1.7.1.3, <1.8.0",
    ],
)