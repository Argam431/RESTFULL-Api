import logging

from bs4 import BeautifulSoup
import requests


logger = logging.getLogger(__name__)


url = 'https://cwur.org/2021-22.php'


def parse(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    
    table = soup.find(id="cwurTable")

    tbody = table.find("tbody")

    universities = []

    for tr in tbody.find_all("tr"):
        columns = tr.find_all("td")

        name = columns[1].text
        country = columns[2].text
        score = columns[-1].text

        universities.append({
            'world_rank': int(columns[0].text),
            'name': name,
            'country': country,
            'score': float(score),
        })

    

    return universities


def scrap():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        logger.debug('received 200 status, now will do parsing')
        return parse(response.text)
    else:
        logger.error(f'unable to get response {response.status_code} {response.content}')


if __name__ == '__main__':
    print(scrap())
