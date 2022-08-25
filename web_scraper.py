import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


class WebScraper:
    @staticmethod
    def economic_times_scraper(url):
        df = pd.DataFrame(columns=['title', 'text', 'subject'])
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        scripts = soup.find_all('script')
        for element in scripts:
            # print(element)
            element = str(element)
            element = element.replace('<script type="application/ld+json">', '')
            element = element.replace('</script>', '')
            try:
                json_data = json.loads(element)
                if json_data.get('headline') is not None:
                    df.loc[0] = [json_data.get('headline'), json_data.get('articleBody'),
                                 json_data.get('articleSection')]
                    return df
            except:
                pass
