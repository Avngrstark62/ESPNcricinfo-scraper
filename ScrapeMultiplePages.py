import os
import pickle
from datetime import datetime, timedelta
from MatchLinksScraper import MatchLinksScraper

curr_date_path = 'D:/databases/cricket_data/curr_date.pkl'
start_date_path = 'D:/databases/cricket_data/start_date.pkl'

def save_date_to_pkl(date, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(date, f)

def load_date_from_pkl(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

if __name__ == '__main__':
    start_date = datetime.strptime('09-10-2024', '%d-%m-%Y')
    save_date_to_pkl(start_date, start_date_path)

    database_url = 'sqlite:///D:/databases/cricket_data.db'
    scraper = MatchLinksScraper(database_url)

    day_decrement = timedelta(days=15)
    curr_date = load_date_from_pkl(curr_date_path)

    if curr_date is None:
        curr_date = load_date_from_pkl(start_date_path)
    
    for _ in range(5):
        print(curr_date)

        date_str = curr_date.strftime('%d-%m-%Y')

        url = f'https://www.espncricinfo.com/live-cricket-match-results?date={date_str}'
        scraper.scrape_data(url)

        curr_date -= day_decrement

        save_date_to_pkl(curr_date, curr_date_path)