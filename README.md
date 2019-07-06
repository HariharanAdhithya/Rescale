# Rescale Web Crawler

## Summary
This is a Python script to crawl and print the links present in the page in a sequential manner. 
It uses a breath-first search technique by printing all the \<a href> links in the initial page and iterates through those links. 

## Compatability
This program is compatible with Python 2 (2.x). It is a download-and-run program with couple of changes according if required by the user.

##Dependencies
There are no dependencies to this project. It runs on the functions of the standard in-build library support. It does not need any external support or installations. Just download and run!!!

## Usage
As mentioned, it is a ready-to-run script. Just mention the web url that you want to start crawling from and aslo the maximum number of threads that can be used as the command line arguments.

`python main.py "http://triplebyte.github.io/web-crawler-test-site/already-passing-tests/" --number_of_threads 20`
