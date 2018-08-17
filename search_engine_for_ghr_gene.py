import requests
from bs4 import BeautifulSoup
# Author:BwZhang


class Search():

    def __init__(self,term):
        self.term=term

    def search_info(self):
        url = ' https://ghr.nlm.nih.gov/search?show=xml&count=1&query=' + self.term   # only search the top result
        webdata = requests.get(url=url).text
        soup = BeautifulSoup(webdata, 'lxml')
        results = soup.select('result')

        with open('summary.txt','a+') as f:
            for result in results:
                for tag in result.find_all(True):
                    if len(tag.contents) == 1:
                        if tag.name == 'symbol' or tag.name == 'name':
                            f.write('gene ' + tag.name + ':' + tag.get_text()+'\n')
                        else:
                            f.write(tag.name + ':' + tag.get_text()+'\n')
                f.write('\n')


if __name__=='__main__':
    item=Search('ABC')
    item.search_info()