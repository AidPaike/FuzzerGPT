import requests, re
from langchain.agents import tool

from lxml import html
from lxml.html.clean import Cleaner
from urllib.parse import urljoin


class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape(self, bug_id):
        url = self.base_url + str(bug_id)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception if status is not 200
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch the webpage: {str(e)}")

        tree = html.fromstring(response.content)

        data = {
            'text': [],
            'links': set()  # Using a set to avoid duplicate links
        }

        # Extract links first
        for link in tree.xpath('//a/@href'):
            full_url = urljoin(self.base_url, link)
            if 'view_bug?bug_id=' in full_url and str(bug_id) not in full_url and full_url != self.base_url:
                data['links'].add(full_url)

        # Remove unwanted elements
        unwanted_classes = ['footer', 'breadcrumbs', 'navbar navbar-default navbar-fixed-top']
        for unwanted_class in unwanted_classes:
            for el in tree.xpath(f"//*[@class='{unwanted_class}']"):
                el.getparent().remove(el)

        # Use Cleaner to remove scripts, style tags, etc.
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        cleaned_tree = cleaner.clean_html(tree)

        # Extract text and check for links
        for element in cleaned_tree.xpath('//body//*'):
            if element.text and element.text.strip():
                data['text'].append(element.text.strip())
                urls = re.findall(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:\\.html|\\.htm)',
                    element.text)
                data['links'].update(urls)

                # Match JDK-XXXXXXX pattern and construct links
                jdk_ids = re.findall('JDK-\d+', element.text)
                for jdk_id in jdk_ids:
                    jdk_link = self.base_url + jdk_id
                    if str(bug_id) not in jdk_link:
                        data['links'].add(jdk_link)

        data['links'] = list(data['links'])  # Convert set back to list
        return data


if __name__ == '__main__':
    # Usage
    scraper = WebScraper('https://bugs.java.com/bugdatabase/view_bug?bug_id=')
    try:
        data = scraper.scrape(8212070)
    except Exception as e:
        print('Error:', e)
