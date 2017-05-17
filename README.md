# python_web_crawler

Simple recursive web-crawler written using only Python's standard libraries.
Parameters:
* _-u_, _--url_ - (*obligatory*) Starting URL, where crawling begins.
* _-v_, _--verbose_ - Prints in STDOUT length of the queue of links to parse.
* _-o_, _--output_ - Should be followed by output file name in order to write
  result into file.
* _-s_, _--subdomains_ - Parse subdomains recovered while crawling.

## Installation

For installation simply download spidy.py file or clone repository:
```
$ git clone https://github.com/phDooY/python_web_crawler.git
$ cd python_web_crawler
```

## Usage

Standard usage, in order to print prettified JSON result in STDOUT:
```
python spidy.py -s -u "http://david.com"
```

If you want to know the status of the queue of links to be parsed, also pass -v
parameter:
```
python spidy.py -s -v -u "http://david.com"
```

In order to save crawling results to file, pass -o "<filename>" parameter:
```
python spidy.py -s -v -o "david.com_crawling.txt" -u "http://david.com"
```