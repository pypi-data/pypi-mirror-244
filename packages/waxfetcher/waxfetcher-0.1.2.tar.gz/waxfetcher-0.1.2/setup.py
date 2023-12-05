from setuptools import setup, find_packages

setup(
    name='waxfetcher',
    version='0.1.2',
    description='waxBlockchain get requests',
    author='Funkaclau',
    author_email='cloudspg@gmail.com',
    packages=['waxfetcher'],
    install_requires=[
        'requests'
    ],
    include_package_data=True
)
