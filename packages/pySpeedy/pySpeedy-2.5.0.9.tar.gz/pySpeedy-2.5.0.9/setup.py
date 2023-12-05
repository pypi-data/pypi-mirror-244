from setuptools import setup, find_packages, Distribution
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open("README.md", 'r') as fh:
    long_description = fh.read()
    
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True


setup(
    name='pySpeedy',
    version='2.5.0.9',
    author='MDBS',
    author_email='simon@mdbs.com.tw',
    description='Speedy Python API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Speedy StarWave',
    packages=find_packages( exclude=['backup', 'build', 'forDoxygen']),
    package_data={'pySpeedy': ['Temp/*.*','pySpeedyAPI_64.dll','pySpeedyAPI_64.so','spdOrderAPI.cp311-win_amd64.pyd','spdQuoteAPI.cp311-win_amd64.pyd']},    
    classifiers=[
    		'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',        
    ],
    
    #distclass=BinaryDistribution
)