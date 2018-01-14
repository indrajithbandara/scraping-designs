import os
import math
import sys
import urllib.request, urllib.error, urllib.parse
import requests
import http.client
import ssl
import re
import multiprocessing as mp
from socket import error as SocketError
import bs4
import concurrent.futures
import pickle
import os
import gzip
import random
import json
import re
import hashlib

try:
  os.mkdir('htmls')
  os.mkdir('hrefs')
except:
  ...
URL = 'http://doujinantena.com'
def html(url): 
  try:
    print(url)
    save_name = 'htmls/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    save_href = 'hrefs/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
    if os.path.exists(save_name) is True:
      return []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    try:
      r = requests.get(url, headers=headers)
    except Exception as e:
      return []
    r.encoding = r.apparent_encoding
    html = r.text
    try:
      open(save_name, 'wb').write( gzip.compress(bytes(html,'utf8')) )
    except OSError:
      return []
    soup = bs4.BeautifulSoup(html)
   
    hrefs = []
    for href in soup.find_all('a', href=True): 
      _url = href['href']
       
      '''http://something.com/.../a'''
      head = '/'.join( url.split('/')[0:3] )
      #print('scan head', head)
      try:
        if '/' == _url[0]:
          _url = head + _url
        if 'http' != _url[0:4]:
          _url = head + '/' + _url
      except IndexError as e:
        continue
      if re.search(r'^http://.*?$', _url) is None: 
        continue
      print(_url)
      hrefs.append(_url)
    #print(hrefs)
    open(save_href, 'w').write( json.dumps(hrefs) )
    return hrefs
  except Exception as ex:
    print(ex)

def main():
  seed = URL
  urls = html(seed) 
 
  try:
    print('try to load pickled urls')
    urls = pickle.loads( gzip.decompress( open('urls.pkl.gz', 'rb').read() ) )
    print(urls)
    print('finished to load pickled urls')
  except FileNotFoundError as e:
    ...
  while True:
    nextUrls = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=128) as executor:
      for rurls in executor.map(html, urls):
        for url in rurls:
          nextUrls.add(url)
    urls = nextUrls
    open('urls.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )
       
main()
