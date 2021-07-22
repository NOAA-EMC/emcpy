from setuptools import setup, find_packages
import os


script_dir = 'src/emcpy/bin'
scripts = [os.path.join(script_dir, x) for x in os.listdir(script_dir)]

setup(
    name='emcpy',
    author='NOAA-EMC',
    version='0.0.1',
    description='A collection of python tools used at EMC',
    url='https://github.com/noaa-emc/emcpy',
    keywords='NOAA, EMC',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={
        '': ['cfg/*'],
    },
    include_package_data=True,
    scripts=scripts,
    python_requires='>= 3.6',
    install_requires=[
        'pyyaml',
        'click',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
