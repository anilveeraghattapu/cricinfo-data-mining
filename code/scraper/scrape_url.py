import os
import requests

from bs4 import BeautifulSoup

import code.bot_settings.settings as bs
from code.entities.score_board import ScoreBoard


def build_score_board(soup):
    sb = ScoreBoard(title=soup.title.text)
    return sb

def get_soup(url, headers):
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        bs.logger.info(f'connected to : {url}')
        return soup
    else:
        bs.logger.error(msg=f'Failed to fetch the page. Status code:{response.text}')


def load_match_date(soup, csb):
    try:
        date_selector = '#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden.ds-rounded-xl.ds-border.ds-border-line > div > div:nth-child(1) > div.ds-px-4.ds-py-3.ds-border-b.ds-border-line > div > div.ds-grow > div.ds-text-tight-m.ds-font-regular.ds-text-typo-mid3'
        result_list = soup.select_one(date_selector).text.strip().split(',')
        csb.date = result_list[-3].strip() + ','+ result_list[-2].strip()
    except Exception as e:
        bs.logger.error(msg=f'load_match_date: {e}')
            

# load team total scores
def load_total_scores(soup, csb):
    try:
        selector =   """#main-container > div.ds-relative > div > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-w-full.ds-bg-fill-content-prime.ds-overflow-hidden.ds-rounded-xl.ds-border.ds-border-line > div > div:nth-child(1) > div.ds-flex"""
        elements = soup.select(selector)
        anchors = elements[0].find_all('a')
        if anchors:
            csb.team_a = anchors[0].text.strip()
            csb.team_b = anchors[1].text.strip()

        strongs = elements[0].find_all('strong')
        if strongs:
            csb.team_a_score = strongs[0].text.strip()
            csb.team_b_score = strongs[1].text.strip()
        
        spans = elements[0].find_all('span')
        if spans:    
            csb.result = spans[4].text.strip()                                                                                             
    except Exception as e:
        bs.logger.error(f'load_total_scores: {e}')

#Load title 
def load_title(soup, csb):
    title = soup.title.text
    
    
def load_match_details(soup, csb):
    try:
        match_details_tab = soup.find('div', string='Match Details').find_next_sibling('div').find('table')
        if match_details_tab:
            rows = match_details_tab.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if cells and len(cells) == 1:
                    csb.location = cells[0].text.strip()

                if cells and len(cells) == 2:
                    if cells[0].text.strip() == 'Toss' :
                        csb.toss = cells[1].text.strip()
                
                    if cells[0].text.strip() == 'Umpires' :
                        csb.umpire_1 = cells[1].find_all('a')[0].text.strip()
                        csb.umpire_2 = cells[1].find_all('a')[1].text.strip()
                    
                    if cells[0].text.strip() == 'Match Referee' :
                        csb.ref = cells[1].text.strip()

                    if cells[0].text.strip() == 'Series' :
                        csb.series = cells[1].text.strip()

                    if cells[0].text.strip() == 'Season' :
                        csb.season = cells[1].text.strip()

                    if cells[0].text.strip() == 'Player Of The Match':
                        csb.potm = cells[1].text.strip()
    except Exception as e:
        bs.logger.error(f'load_match_details: {e}')

def scrape_espn(url):
    headers = {
        'User-Agent': bs.get_random_ua()
    }
    soup = get_soup(url, headers)
    if soup:
        current_score_board = build_score_board(soup)
                
        load_title(soup, current_score_board)
        load_total_scores(soup, current_score_board)
        load_match_details(soup, current_score_board)
        load_match_date(soup,current_score_board)
        print(current_score_board)
