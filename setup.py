import os

from setuptools import find_packages, setup

import dc_signup_form

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version():
    return dc_signup_form.__version__


setup(
    name="dc_signup_form",
    version=get_version(),
    author="chris48s",
    packages=find_packages(),
    include_package_data=True,
    description="Email Signup form component for use on DC websites",
    url="https://github.com/DemocracyClub/dc_signup_form",
    install_requires=[
        'requests',
        'Django >=3.2,<4.3',
        'psycopg2-binary',
    ],
    setup_requires=["wheel"],
)
