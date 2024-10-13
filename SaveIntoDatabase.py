import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CricketDatabase:
    class MatchInfo(Base):
        __tablename__ = 'match_info'
        
        id = Column(Integer, primary_key=True)
        ground = Column(String)
        toss = Column(String)
        series = Column(String)
        season = Column(String)
        match_days = Column(String)

    class BattingData(Base):
        __tablename__ = 'batting_data'
        
        id = Column(Integer, primary_key=True)
        match_id = Column(Integer, ForeignKey('match_info.id'))
        team_name = Column(String)
        player = Column(String)
        dismissal = Column(String)
        runs = Column(String)
        balls = Column(String)
        maidens = Column(String)
        fours = Column(String)
        sixes = Column(String)
        strike_rate = Column(String)

    class BowlingData(Base):
        __tablename__ = 'bowling_data'
        
        id = Column(Integer, primary_key=True)
        match_id = Column(Integer, ForeignKey('match_info.id'))
        team_name = Column(String)
        player = Column(String)
        overs = Column(String)
        maidens = Column(String)
        runs = Column(String)
        wickets = Column(String)
        economy = Column(String)
        dots = Column(String)
        fours = Column(String)
        sixes = Column(String)
        wides = Column(String)
        no_balls = Column(String)

    def __init__(self, match_id, db_name='cricket_data.db'):
        self.match_id = match_id
        self.engine = create_engine(f'sqlite:///D:/databases/{db_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_match_info(self, match_id, match_info):
        session = self.Session()
        match_record = self.MatchInfo(
            id=match_id,
            ground=match_info['Ground'],
            toss=match_info['Toss'],
            series=match_info['Series'],
            season=match_info['Season'],
            match_days=match_info['Match Days']
        )
        session.add(match_record)
        session.commit()
        return match_record.id

    def save_batting_data(self, match_id, batting_data):
        session = self.Session()
        for player in batting_data:
            batting_record = self.BattingData(
                match_id=match_id,
                team_name=player['Team Name'],
                player=player['Player'],
                dismissal=player['Dismissal'],
                runs=player['Runs'],
                balls=player['Balls'],
                maidens=player['Maidens'],
                fours=player['Fours'],
                sixes=player['Sixes'],
                strike_rate=player['Strike Rate']
                
            )
            session.add(batting_record)
        session.commit()

    def save_bowling_data(self, match_id, bowling_data):
        session = self.Session()
        for player in bowling_data:
            bowling_record = self.BowlingData(
                match_id=match_id,
                team_name=player['Team Name'],
                player=player['Player'],
                overs=player['Overs'],
                maidens=player['Maidens'],
                runs=player['Runs'],
                wickets=player['Wickets'],
                economy=player['Economy'],
                dots=player['Dots'],
                fours=player['Fours'],
                sixes=player['Sixes'],
                wides=player['Wides'],
                no_balls=player['No Balls']
            )
            session.add(bowling_record)
        session.commit()

    def save_into_database(self):
        match_info = pd.read_csv('temp/match_details.csv').set_index('Key')['Value'].to_dict()  # Assuming one match per CSV
        match_id = self.save_match_info(self.match_id, match_info)
        os.remove('temp/match_details.csv')

        # Load batting data
        for filename in os.listdir('temp/batting_data'):
            if filename.endswith('_batting.csv'):
                file_path = os.path.join('temp/batting_data', filename)
                batting_data = pd.read_csv(file_path).to_dict(orient='records')
                self.save_batting_data(match_id, batting_data)
                os.remove(file_path)

        # Load bowling data
        for filename in os.listdir('temp/bowling_data'):
            if filename.endswith('_bowling.csv'):
                file_path = os.path.join('temp/bowling_data', filename)
                bowling_data = pd.read_csv(file_path).to_dict(orient='records')
                self.save_bowling_data(match_id, bowling_data)
                os.remove(file_path)

        print(f"Data has been successfully saved to the database.")