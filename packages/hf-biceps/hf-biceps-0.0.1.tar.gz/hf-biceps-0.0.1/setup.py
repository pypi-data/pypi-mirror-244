from setuptools import setup, find_packages

setup(
    name='hf-biceps',
    version='0.0.1',
    authors = [
        {'name': "Niels Pichon", 'email': "niels@biceps.ai"},
    ],
    packages=find_packages(
        # All keyword arguments below are optional:
        where='src',  # '.' by default
        include=['biceps*']
    )
)