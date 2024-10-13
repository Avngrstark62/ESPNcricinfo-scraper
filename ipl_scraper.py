# from CricketScoreboardScraper import CricketScoreboardScraper
# from SaveIntoDatabase import CricketDatabase
# from IPLLinksScraper import IPLLinksScraper
# import pickle
# import os

# def save_match(index, match_link, season):
#     if os.path.exists('scraped_links.pkl'):
#         with open('scraped_links.pkl', 'rb') as f:
#             scraped_links = pickle.load(f)
#     else:
#         scraped_links = []
    
#     if os.path.exists('unscraped_links.pkl'):
#         with open('unscraped_links.pkl', 'rb') as f:
#             unscraped_links = pickle.load(f)
#     else:
#         unscraped_links = []
    
#     if match_link not in scraped_links:
#         print(f'Scraping Season {season} Match No. {index+1}')
#         url = "https://www.espncricinfo.com"+match_link
#         try:
#             match_scraper = CricketScoreboardScraper(url)
#             match_scraper.scrape()
#             database = CricketDatabase()
#             database.save_into_database()
#             scraped_links.append(match_link)
#         except Exception as e:
#             unscraped_links.append(match_link)
#             print(f'Match No. {index+1} is not Scraped or interupted')
#         print('-'*100)
    
#     with open('scraped_links.pkl', 'wb') as f:
#         pickle.dump(scraped_links, f)
    
#     with open('unscraped_links.pkl', 'wb') as f:
#         pickle.dump(unscraped_links, f)

# def save_season(url):
#     links_scraper = IPLLinksScraper(url)
#     links_scraper.scrape()
#     match_links = links_scraper.get_match_links()
#     if 'indian-premier-league' in url:
#         season = url.split('-')[3]
#     elif 'ipl' in url:
#         season = url.split('-')[1]

#     return match_links, season

# season_urls = [
#     "https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/ipl-2021-1249214/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/ipl-2019-1165643/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/ipl-2018-1131611/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/ipl-2017-1078425/match-schedule-fixtures-and-results",
#     "https://www.espncricinfo.com/series/ipl-2016-968923/match-schedule-fixtures-and-results",
# ]



# if __name__ == "__main__":
#     for url in season_urls:
#         match_links, season = save_season(url)
#         for i, match_link in enumerate(match_links):
#             save_match(i, match_link, season)


# if __name__ == "__main__":
#         url = "https://www.espncricinfo.com/series/ireland-vs-south-africa-2024-25-1431081/ireland-vs-south-africa-3rd-odi-1431090/full-scorecard"
#         try:
#             match_scraper = CricketScoreboardScraper(url)
#             match_scraper.scrape()
#             database = CricketDatabase()
#             database.save_into_database()
#         except Exception as e:
#             print(e)