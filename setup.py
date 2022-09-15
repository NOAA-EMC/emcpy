import setuptools
setuptools.setup(
    name='emcpy',
    version='0.0.1',
    description='A collection of python tools used at EMC',
    author='NOAA-EMC',
    author_email='rahul.mahajan@noaa.gov',
    url='https://github.com/noaa-emc/emcpy',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Typing :: Typed'],
    python_requires='>=3.6',
    install_requires=[
        'pyyaml>=6.0',
        'pycodestyle>=2.8.0',
        'netCDF4>=1.5.3',
        'matplotlib>=3.5.2',
        'cartopy>=0.20.2',
        'scikit-learn>=1.0.2',
        'xarray>=0.11.3',
    ]
#    entry_points={
#        'console_scripts': [
#            'emcpy_tests = emcpy.test_plots:main',
#        ],
#    },
)
