import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class CricketScoreboardScraper:
    def __init__(self, url):
        self.url = url
        self.temp_dir = 'temp'
        os.makedirs(self.temp_dir, exist_ok=True)
        self.batting_data_folder = os.path.join(self.temp_dir, 'batting_data')
        self.bowling_data_folder = os.path.join(self.temp_dir, 'bowling_data')
        os.makedirs(self.batting_data_folder, exist_ok=True)
        os.makedirs(self.bowling_data_folder, exist_ok=True)

        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.teams = ['team1', 'team2']
    
    def scrape_team_names(self):
        soup = self.soup

        team_divs = soup.find_all('div', class_='ds-relative ds-w-full ds-scrollbar-hide ds-py-2')
        team_names = []
        # Loop through each team_div and find span with 'ds-text-tight-xs' class
        for div in team_divs:
            team_spans = div.find_all('span', class_='ds-text-tight-xs')
            # Extract the text from each span and add it to the list
            for span in team_spans:
                team_names.append(span.get_text(strip=True))
        team_names = [team_name.replace('Innings', '').strip() for team_name in team_names if 'Innings' in team_name]

        self.teams[0] = team_names[0]
        self.teams[1] = team_names[1]
    
    def scrape_batting_data(self):
        # Send a request to fetch the HTML content
        soup = self.soup
        # Find all batting scorecard tables
        tables = soup.find_all('table', class_='ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table')

        # Prepare to store the data for each team
        team_data = {}

        # Loop through each table (for both innings)
        for i, table in enumerate(tables):
            team_name = self.teams[i]

            # Prepare to store data for the current team if it doesn't exist in the dictionary
            if team_name not in team_data:
                team_data[team_name] = []

            # Loop through each row in the table body
            for row in table.find('tbody').find_all('tr'):
                cells = row.find_all('td')

                # Check if the row has the correct number of cells
                if len(cells) == 8:  # Adjust based on expected number of columns
                    player_data = {
                        'Player': cells[0].get_text(strip=True),
                        'Dismissal': cells[1].get_text(strip=True),
                        'Runs': cells[2].get_text(strip=True),
                        'Balls': cells[3].get_text(strip=True),
                        'Maidens': cells[4].get_text(strip=True),
                        'Fours': cells[5].get_text(strip=True),
                        'Sixes': cells[6].get_text(strip=True),
                        'Strike Rate': cells[7].get_text(strip=True),
                        'Team Name': team_name
                    }
                    team_data[team_name].append(player_data)
                
                elif len(cells) == 1 and 'Did not bat' in cells[0].get_text():
                    did_not_bat_players = []
                    
                    # Find all players in the "Did not bat" section
                    for player_tag in cells[0].find_all('a'):
                        player_name = player_tag.get_text(strip=True)
                        did_not_bat_players.append(player_name)
                    
                    # Add "Did not bat" players to the team data
                    for player in did_not_bat_players:
                        player_data = {
                            'Player': player,
                            'Dismissal': 'Did not bat',
                            'Runs': None,
                            'Balls': None,
                            'Maidens': None,
                            'Fours': None,
                            'Sixes': None,
                            'Strike Rate': None,
                            'Team Name': team_name
                        }
                        team_data[team_name].append(player_data)

        # Save the data for each team in separate CSV files
        for team_name, players in team_data.items():
            if players:  # Only save if there are players data
                df = pd.DataFrame(players)
                # sanitized_team_name = team_name.replace(" ", "_").replace("/", "-")
                df.to_csv(f'{self.batting_data_folder}/{team_name}_batting.csv', index=False)
                print(f"Batting Data for {team_name} has been successfully saved to '{team_name}_batting.csv'.")

    def scrape_bowling_data(self):
        # Send a request to fetch the HTML content
        soup = self.soup

        # Find all bowling scorecard tables
        tables = soup.find_all('table', class_='ds-w-full ds-table ds-table-md ds-table-auto')

        # Prepare to store the data for each team
        team_data = {}

        # Loop through each table (for both innings)
        for i, table in enumerate(tables):
            # Ensure we're only processing bowling tables
            if "Bowling" in table.find('thead').get_text():
                j=1
                if i==1:
                    j=0
                team_name = self.teams[j]  # Use team indices

                # Prepare to store data for the current team if it doesn't exist in the dictionary
                if team_name not in team_data:
                    team_data[team_name] = []

                # Loop through each row in the table body
                for row in table.find('tbody').find_all('tr'):
                    cells = row.find_all('td')

                    # Check if the row has the correct number of cells (adjust based on expected number of columns)
                    if len(cells) >= 11:  # Ensure that we have enough columns based on your HTML structure
                        player_data = {
                            'Player': cells[0].get_text(strip=True),
                            'Overs': cells[1].get_text(strip=True),
                            'Maidens': cells[2].get_text(strip=True),
                            'Runs': cells[3].get_text(strip=True),
                            'Wickets': cells[4].get_text(strip=True),
                            'Economy': cells[5].get_text(strip=True),
                            'Dots': cells[6].get_text(strip=True),
                            'Fours': cells[7].get_text(strip=True),
                            'Sixes': cells[8].get_text(strip=True),
                            'Wides': cells[9].get_text(strip=True),
                            'No Balls': cells[10].get_text(strip=True),
                            'Team Name': team_name
                        }
                        team_data[team_name].append(player_data)

        # Save the data for each team in separate CSV files
        for team_name, players in team_data.items():
            if players:  # Only save if there are players data
                df = pd.DataFrame(players)
                # sanitized_team_name = team_name.replace(" ", "_").replace("/", "-")
                df.to_csv(f'{self.bowling_data_folder}/{team_name}_bowling.csv', index=False)
                print(f"Bowling Data for {team_name} has been successfully saved to '{team_name}_bowling.csv'.")

    def scrape_match_info(self):
        # Make a request to fetch the HTML content
        soup = self.soup

        # Extracting information
        match_info = {}

        # Extract the match ground
        ground_cell = soup.find('td', colspan='2')  # This finds the cell containing the ground information
        match_info['Ground'] = ground_cell.find('a').text.strip() if ground_cell and ground_cell.find('a') else None

        # Extract toss information
        toss_info = soup.find('td', string='Toss').find_next_sibling('td')
        match_info['Toss'] = toss_info.text.strip() if toss_info else None

        # Extract series information
        series_info = soup.find('td', string='Series').find_next('td').find('a')
        match_info['Series'] = series_info.text.strip() if series_info else None

        # Extract season
        season_info = soup.find('td', string='Season').find_next('td').find('a')
        match_info['Season'] = season_info.text.strip() if season_info else None

        # Extract match days
        match_days = soup.find('td', string='Match days').find_next('td')
        match_info['Match Days'] = match_days.text.strip() if match_days else None

        # Save the match details to a CSV file
        df = pd.DataFrame(match_info.items(), columns=['Key', 'Value'])
        df.to_csv(os.path.join(self.temp_dir, 'match_details.csv'), index=False)

        print(f"Match Data has been successfully saved to 'match_details.csv'.")
    

    def scrape(self):
        self.scrape_team_names()
        self.scrape_match_info()
        self.scrape_batting_data()
        self.scrape_bowling_data()