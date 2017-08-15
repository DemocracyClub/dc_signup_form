import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dc_signup_form',
    version='1.0.0',
    author="chris48s",
    packages=find_packages(),
    include_package_data=True,
    description='Email Signup form component for use on DC websites',
    url='https://github.com/DemocracyClub/dc_signup_form',
    install_requires=[
        'requests',
    ]
)
