from typing import List, Dict
import requests
import json
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlencode, parse_qs
import re

url='https://www.uniprot.org/uniprot/?query=p53&sort=score'
webdata=requests.get(url=url).text

soup=BeautifulSoup(webdata,'lxml')
print(soup.select('td'))
for tag in soup.find_all('td'):
    if len(tag.contents)==1:
        print(tag.name,tag.get_text())
#ids=soup.select('td.entryID')
#print(ids)
