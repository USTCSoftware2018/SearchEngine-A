import requests
import json
from bs4 import BeautifulSoup
# Author:BwZhang


class Search():

    def __init__(self,term):
        self.term = term

    def search_info(self):
        url = ' https://ghr.nlm.nih.gov/search?show=xml&count=1&query=' + self.term   # only search the top result
        webdata = requests.get(url=url).text
        soup = BeautifulSoup(webdata, 'lxml')
        results = soup.select('result')

        results_list = []

        for result in results:
            detail = {}
            detail['dbname'] = 'ghr_gene'
            for tag in result.find_all(True):
                if len(tag.contents) == 1:
                    if tag.name == 'name':
                        detail['gene name'] = tag.get_text()
                        temp_detail = json.dumps(detail)
                        join_detail = json.loads(temp_detail)
                        results_list.append(join_detail)
                        detail.clear()

                    elif tag.name == 'symbol':
                        detail['gene symbol'] = tag.get_text()

                    else:
                        detail[tag.name] = tag.get_text()

        return results_list


if __name__ == '__main__':
    item = Search('ABC')
    result = item.search_info()
    print(result)