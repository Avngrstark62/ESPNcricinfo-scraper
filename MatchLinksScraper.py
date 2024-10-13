import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import pickle
from datetime import datetime, timedelta

# Define the Matches model
Base = declarative_base()

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # New id column as primary key
    link = Column(String, unique=True)  # Link column set to be unique
    team1_name = Column(String)
    team1_score = Column(String)
    team2_name = Column(String)
    team2_score = Column(String)
    result = Column(String)

curr_date_path = 'D:/databases/cricket_data/curr_date.pkl'
start_date_path = 'D:/databases/cricket_data/start_date.pkl'

def save_pkl_file(file, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(file, f)

def load_pkl_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

class MatchLinksScraper:
    def __init__(self, database_url, teams_to_scrape, scrape_tests=False):
        # Database setup
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)

        # Create a session
        self.Session = sessionmaker(bind=self.engine)

        self.teams_to_scrape = teams_to_scrape
        self.scrape_tests = scrape_tests
    
    def scrape_links_from_page(self, url):
        # Fetch the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all match blocks
        match_blocks = soup.find_all('div', class_='ds-px-4 ds-py-3')

        # Loop through each match block and extract required details
        for match_block in match_blocks:
            session = self.Session()
            # Extract the match link
            link = match_block.find('a', href=True)['href']

            if 'women' in link:
                continue
            
            # Extract team names and scores
            teams = match_block.find_all('p', class_='ds-text-tight-m ds-font-bold ds-capitalize ds-truncate')
            scores = match_block.find_all('strong')
            
            team1_name = teams[0].text.strip()  # Team 1 name
            team2_name = teams[1].text.strip()  # Team 2 name

            not_a_league = True
            leagues_list = ['indian-premier-league', 'big-bash-league', 'the-hundred-men', 'caribbean-premier-league', 'bangladesh-premier-league', 'pakistan-super-league', 'major-league-cricket', 'lanka-premier-league', 'international-league-t20', 'sa20', 'global-t20-canada', 'super-smash']
            for league in leagues_list:
                if league in link:
                    not_a_league = False

            if (team1_name not in self.teams_to_scrape) and (team2_name not in self.teams_to_scrape) and not_a_league:
                continue

            try:
                team1_score = scores[0].text.strip()  # Team 1 score
            except:
                team1_score = ''
            
            try:
                team2_score = scores[1].text.strip()  # Team 2 score
            except:
                team2_score = ''
        
            try:
                # Extract the result
                result = match_block.find('p', class_='ds-text-tight-s ds-font-medium ds-truncate ds-text-typo').text.strip()
            except:
                result = 'No result'

            if self.scrape_tests == False:
                if '&' in team1_score or '&' in team2_score:
                    continue
            
            match_instance = Match(
                link=link,
                team1_name=team1_name,
                team1_score=team1_score,
                team2_name=team2_name,
                team2_score=team2_score,
                result=result
            )
            
            # Add the match instance to the session
            session.add(match_instance)
            try:
                session.commit()
            except Exception as e:
                print(e)
            # Close the session
            session.close()
    
    def scrape_multiple_pages(self):
        start_date = datetime.strptime('09-10-2024', '%d-%m-%Y')
        save_pkl_file(start_date, start_date_path)

        day_decrement = timedelta(days=15)
        curr_date = load_pkl_file(curr_date_path)

        if curr_date is None:
            curr_date = load_pkl_file(start_date_path)
        
        for _ in range(20):
            print(curr_date)
    
            date_str = curr_date.strftime('%d-%m-%Y')
    
            url = f'https://www.espncricinfo.com/live-cricket-match-results?date={date_str}&quick_class_id=t20'
            self.scrape_links_from_page(url)
    
            curr_date -= day_decrement
    
            save_pkl_file(curr_date, curr_date_path)
        print('Execution Finished')

    def get_match_links(self):
        session = self.Session()
        try:
            # Query the database to get both id and link from the matches table
            match_links = session.query(Match.id, Match.link).order_by(None).all()
            
            # Create a dictionary with id as the key and link as the value
            match_links_dict =  {match.id: match.link for match in match_links}
            return sorted(match_links_dict.items())
        finally:
            session.close()



if __name__ == '__main__':
    database_url = 'sqlite:///D:/databases/cricket_data.db'
    teams_to_scrape = ['India', 'Australia', 'South Africa', 'New Zealand', 'England', 'Sri Lanka', 'West Indies', 'Pakistan', 'Bangladesh', 'Afganistan', 'Scotland', 'Ireland', 'Zimbabwe', 'Netherlands']
    links_scraper = MatchLinksScraper(database_url, teams_to_scrape)
    links_scraper.scrape_multiple_pages()
    match_links = links_scraper.get_match_links()

    match_links_path = 'D:/databases/cricket_data/match_links.pkl'
    save_pkl_file(match_links, match_links_path)