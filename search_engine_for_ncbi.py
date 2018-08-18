import requests
import json
from bs4 import BeautifulSoup


class SearchTerm(object):

    def __init__(self, term):
        self.term = term
        self.dbnames = []
        self.count = []

    def search_query(self): # find all databases which are concerning with the item
        url_query = 'https://eutils.ncbi.nlm.nih.gov/gquery' + '?term=' + self.term + '&retmode=xml'
        webdata = requests.get(url=url_query).text
        soup = BeautifulSoup(webdata, 'lxml')
        names = soup.select('dbname')
        nums = soup.select('count')

        for name, num in zip(names, nums):
            self.dbnames.append(name.get_text())
            self.count.append(num.get_text())

    def search_summary(self):
        base_url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' +'&usehistory=y' + '&term=' + self.term + '&db='
        List=[]
        for name,num in zip(self.dbnames,self.count):
            url_search=base_url+name
            webdata = requests.get(url=url_search).text
            soup = BeautifulSoup(webdata, 'lxml')
            webenv = soup.select('webenv')[0].get_text()
            query_key = soup.select('querykey')[0].get_text()

            if int(num)==0:
                continue
            if int(num)>=20:           # set the max numbers to get in a database
                num='20'
            url_summary = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?' + 'db=' + name + '&WebEnv=' + webenv + \
                          '&query_key=' + query_key + '&retstart=0'+'&retmax=' + str(num)

            webdata = requests.get(url=url_summary).text
            soup = BeautifulSoup(webdata, 'lxml')

            tag_name = []
            print(name)
            result = {}

            for tag in soup.find_all(True):

                result['dbname']=name
                if tag.name!='item' and tag.name in tag_name:
                    del tag_name[:]
                    results=json.dumps(result)
                    join_result=json.loads(results)
                    List.append(join_result)
                    result.clear()

                if len(tag.contents) == 1 and tag.name != 'html' and tag.name != 'error' and tag.name != 'sampledata':

                    if tag.name == 'item':
                        item_name=tag.get('name')
                        tag_name.append(tag.name)

                        if item_name in result:
                            result[item_name] += tag.get_text()

                        else:
                            result[item_name]=tag.get_text()

                    else:

                        tag_name.append(tag.name)
                        if tag.name in result:
                            result[tag.name] += tag.get_text()
                        else:
                            result[tag.name] = tag.get_text()

            results = json.dumps(result)
            join_result = json.loads(results)
            List.append(join_result)
            result.clear()

        return List


if __name__ == '__main__':
    term = SearchTerm(input("Input the term you would like to search:"))
    term.search_query()
    print(term.search_summary())