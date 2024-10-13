from CricketScoreboardScraper import CricketScoreboardScraper
from SaveIntoDatabase import CricketDatabase
import os
import pickle

def save_pkl_file(file, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(file, f)

def load_pkl_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

if __name__ == '__main__':
    match_links_path = 'D:/databases/cricket_data/match_links.pkl'
    match_links = load_pkl_file(match_links_path)

    for match_id, match_link in match_links:
        print(f"ID: {match_id}, Link: {match_link}")
        url = "https://www.espncricinfo.com" + match_link
        try:
            match_scraper = CricketScoreboardScraper(url)
            match_scraper.scrape()
            database = CricketDatabase(match_id)
            database.save_into_database()
        except Exception as e:
            print(e)
    
    print('Saved all the data from match_links')