I wrote this script for download TV series from link3 local server.

## Please Follow this steps:
+ cd to source directory
+ pip install -r requirements.txt
+ change the value of **config.py** file
+ python link3TvSeriesDownloader.py

## Steps for making installer
+ pip install py2exe
+ uncomment link3TvSeriesDownloader.py main for exe & comment existing one
+ python setup.py py2exe