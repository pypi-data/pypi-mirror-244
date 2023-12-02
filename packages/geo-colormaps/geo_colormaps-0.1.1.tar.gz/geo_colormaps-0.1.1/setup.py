#!/usr/bin/python

# geo_colormap
import os
import glob
from setuptools import find_packages, setup

def get_data_files(base_path, dir):
    data_files = []

    for path, _, files in os.walk(dir):
        list_entry = (base_path + path, [os.path.join(path, f) for f in files if not f.startswith('.')])
        data_files.append(list_entry)

    return data_files


setup(name='geo_colormaps',
        version='0.1.1',
        description='geo_colormap is a collection of standard weather/ocean colormaps, for creating plots using `matplotlib`. It allows easy additions of custom colormaps using csv tables.',
        author='Guangzhi XU',
        author_email='xugzhi1987@gmail.com',
        url='https://github.com/Xunius/geo_colormaps',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Atmospheric Science'
            ],
        install_requires=[
            "numpy",
            "matplotlib",
            "jinja2"
        ],
        packages=find_packages(include=['geo_colormaps', 'geo_colormaps.*']),
        include_package_data=True,
        package_data={'tests': ['*'], 'data': ['*'], 'examples': ['*'], 'images': ['*.png'], 'colormap_defs': ['*']},
        data_files=[('data', glob.glob('data/*')),] +\
                get_data_files('images', 'images') +\
                get_data_files('colormap_defs', 'colormap_defs'),
        python_requires = ">=3.5",
        license='GPL-3.0-or-later'
        )

