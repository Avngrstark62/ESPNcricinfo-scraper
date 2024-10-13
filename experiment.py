import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = 'sqlite:///D:/databases/cricket_data.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Matches model
class Match(Base):
    __tablename__ = 'matches'
    
    link = Column(String, primary_key=True)  # Assuming link is unique
    team1_name = Column(String)
    team1_score = Column(String)
    team2_name = Column(String)
    team2_score = Column(String)
    result = Column(String)

Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Example URL (replace with the actual URL)
url = 'https://www.espncricinfo.com/live-cricket-match-results'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all match blocks
match_blocks = soup.find_all('div', class_='ds-px-4 ds-py-3')

# Loop through each match block and extract required details
for i, match_block in enumerate(match_blocks):
    # Extract the match link
    link = match_block.find('a', href=True)['href']
    
    # Extract team names and scores
    teams = match_block.find_all('p', class_='ds-text-tight-m ds-font-bold ds-capitalize ds-truncate')
    scores = match_block.find_all('strong')
    
    team1_name = teams[0].text.strip()  # Team 1 name
    team2_name = teams[1].text.strip()  # Team 2 name

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


# Commit the session to save data into the database
session.commit()

# Close the session
session.close()