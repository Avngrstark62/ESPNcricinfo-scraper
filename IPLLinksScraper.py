import requests
from bs4 import BeautifulSoup

class IPLLinksScraper:
    def __init__(self, url):
        if 'indian-premier-league' in url:
            self.season = url.split('-')[3]
        elif 'ipl' in url:
            self.season = url.split('-')[1]
        self.url = url
        self.match_links = []
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def scrape(self):
        all_links = self.soup.find_all('a', class_='ds-no-tap-higlight')
        # Extract and filter the href attributes (match links) for the specified IPL season
        for link in all_links:
            match_url = link.get('href')
            if (f'indian-premier-league-{self.season}' in match_url) or (f'ipl-{self.season}' in match_url):
                self.match_links.append(match_url)

    def get_match_links(self):
        return self.match_links