from setuptools import setup, find_packages

setup(
    name = 'cameo_geo_query',
    version = '0.0.7',
    description='This is cameo_geo_query',
    url = '',
    author = 'bear',
    author_email='panda19931217@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'geopy',
        'plotly'
    ]
)
