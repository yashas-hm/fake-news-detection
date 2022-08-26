import re

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


# india tv
# indian express
# livemint
# livelaw
# economic times/india times
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

    @staticmethod
    def gov_site(url):
        df = pd.DataFrame(columns=['title', 'text', 'subject'])
        headers = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/51.0.2704.103 Safari/537.36', }
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.content, 'html.parser')
        scripts = soup.find_all('input')
        title = ''
        subject = 'Policy'
        text = ''
        for index in range(len(scripts)):
            element = str(scripts[index])
            print(element)
            if element.find('name="ltrTitlee"') != -1 and element.find('id="ltrTitlee"') != -1:
                element = element.replace('<input', '')
                element = element.replace('type="hidden"', '')
                element = element.replace('name="ltrTitlee"', '')
                element = element.replace('value="', '')
                element = element.replace('id="ltrTitlee"', '')
                element = element.replace('"/>', '')
                title = element
            elif element.find('name="ltrDescriptionn"') != -1 and element.find('id="ltrDescriptionn"'):
                element = element.replace('<input', '')
                element = element.replace('type="hidden"', '')
                element = element.replace('name="ltrDescriptionn"', '')
                element = element.replace('id="ltrDescriptionn"', '')
                element = element.replace('value="', '')
                element = element.replace('\'/>', '')
                element = re.sub(r'^&lt;[a-zA-Z\/;&"=_.: ].*&gt;$', '', element)
                text = element

        df.loc[0] = [title, text, subject]
        print(df.text[0])
        print(df.title[0])
        return df


# a = WebScraper.economic_times_scraper('https://economictimes.indiatimes.com/news/india/sc-sets-aside-mp-hc-verdict-on-discharge-of-rape-accused-says-its-utterly-incomprehensible/articleshow/93659916.cms')
# a = WebScraper.gov_site('https://pib.gov.in/PressReleaseIframePage.aspx?PRID=1854323')
# print(a)
