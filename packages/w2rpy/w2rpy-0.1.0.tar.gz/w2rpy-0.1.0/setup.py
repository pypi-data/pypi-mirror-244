# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:06:42 2023

@author: lrussell
"""

from setuptools import setup, find_packages

setup(
    name='w2rpy',
    version='0.1.0',
    packages=find_packages(),
    python_requires='<=3.11',
    
    install_requires=[
        'pandas',
        'numpy',
        'shapely',
        'geopandas',
        'rasterio',
        'pysheds',
        'scipy',
        'spyder',
        'spyder-kernels==2.5',
        'jupyterlab',
        'ipywidgets',
        'notebook'],
        
    entry_points={'console_scripts': []},
)