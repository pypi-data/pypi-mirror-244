from setuptools import setup, find_packages

setup(
    name='waxfetcher',
    version='0.1.0',
    description='waxBlockchain get requests',
    author='Funkaclau',
    author_email='cloudspg@gmail.com',
    packages=find_packages(),
    install_requires=[
        'time',
        'json',
        'requests'
    ],
)
