import requests
from bs4 import BeautifulSoup


class SearchTerm():

    def __init__(self,term):
        self.term=term

    def search_query(self): # find all databases which are concerning with the item
        url_query = 'https://eutils.ncbi.nlm.nih.gov/gquery' + '?term=' + self.term + '&retmode=xml'
        webdata = requests.get(url=url_query).text
        soup = BeautifulSoup(webdata, 'lxml')
        names = soup.select('dbname')
        nums = soup.select('count')
        # print(names, nums)
        self.dbnames, self.count = [], []
        for name, num in zip(names, nums):
            self.dbnames.append(name.get_text())
            self.count.append(num.get_text())
            #print(name.get_text(), num.get_text())

    def search_summary(self):
        base_url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' +'&usehistory=y' + '&term=' + self.term + '&db='

        for name,num in zip(self.dbnames,self.count):
            url_search=base_url+name
            webdata = requests.get(url=url_search).text
            soup = BeautifulSoup(webdata, 'lxml')
            webenv = soup.select('webenv')[0].get_text()
            query_key = soup.select('querykey')[0].get_text()
            #print(webenv, query_key)
            if int(num==0):
                continue
            if int(num)>=20:           # set the max numbers to get in a database
                url_summary = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?' + 'db=' + name + '&WebEnv=' + webenv + \
                          '&query_key=' + query_key + '&retstart=0'+'&retmax=' + str(20)
            else:
                url_summary = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?' + 'db=' + name + '&WebEnv=' + webenv + \
                              '&query_key=' + query_key + '&retstart=0'+'&retmax='+str(num)
            webdata = requests.get(url=url_summary).text
            soup = BeautifulSoup(webdata, 'lxml')
            # print(soup)
            tag_name = []
            print(name)
            with open("summary.txt",'a+') as f:             # write data
                f.write(name+':\n')
                for tag in soup.find_all(True):
                    if tag.name!='item' and tag.name in tag_name:
                        del tag_name[:]
                        f.write('\n')
                    if len(tag.contents) == 1 and tag.name != 'html':
                        if tag.name=='item':
                            item_name=tag.get('name')
                            tag_name.append(tag.name)
                            string = tag.name + ':'+ item_name + ":" + tag.get_text()
                            f.write(string.encode("gbk","ignore").decode("UTF-8",'ignore') + '\n')
                        else:
                            tag_name.append(tag.name)
                            string = tag.name + ":" + tag.get_text()
                            f.write(string.encode("gbk", "ignore").decode("UTF-8", 'ignore') + '\n')

if __name__=='__main__':
    term=SearchTerm(input("Input the item you want to search:"))
    term.search_query()
    term.search_summary()