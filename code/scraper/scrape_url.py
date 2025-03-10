import os
import requests
import re

from bs4 import BeautifulSoup

import code.bot_settings.settings as bs
from code.entities.score_board import ScoreBoard

def cache_page():
    pass

def build_score_board(soup):
    sb = ScoreBoard(title=soup.title.text)
    return sb

def get_soup(url='', headers= ''):
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        bs.logger.info(f'{url}')
        return soup
    else:
        bs.logger.error(msg=f'Failed to fetch the page. Status code:{response.text}')

def get_soup2(url=None, headers=None):
    with open(os.path.join(bs.cache_dir, 'page.html'), 'r', encoding='utf-8') as file:
        html_content = file.read()
    return BeautifulSoup(html_content, 'html.parser')

def load_scores(soup, csb):
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        table_id = table.get('id', 'No ID')
        rows = table.find_all('tr')
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        #print(f"Table {i + 1} - ID: {table_id}, Rows: {len(rows)}, headers: {headers}")
        
        if i == 0:
            for row in table.find_all('tr'):
                print('\n')
                for cell in row.find_all(['td', 'th']):
                    if  len(cell.text.strip()) > 0:
                        print(cell.text.strip(), end=' | ')
            
        #for attr, value in table.attrs.items():
        #    print(f"  {attr}: {value}")
# load team total scores
def load_total_scores(soup, csb):
    div = soup.find('div',  class_='ds-w-2/3')
    #csb.target = div.find('span', class_='ds-text-compact-s').text.strip()
    csb.result = div.find('p', class_='ds-text-tight-s').text.strip()
    scores_div = div.find_all('div', class_='ci-team-score')
    # team a div
    csb.team_a = scores_div[0].find('a').text.strip()
    csb.team_a_score = scores_div[0].find('strong').text.strip()
    # team b div
    csb.team_b = scores_div[1].find('a').text.strip()
    csb.target = scores_div[1].find_all('span')[1].text.strip()
    #for e in scores_div[1].find_all('span'):
    #   print(e.text)

    csb.team_b_score = scores_div[1].find('strong').text.strip()
    #print(len(scores_div))

#Load title and other details form the title
def load_title(soup, csb):
    #pattern = r'^(?P<team_a_code>[A-Z]+) vs (?P<team_b_code>[A-Z]+) Cricket Scorecard, (?P<match>[^,]+) at (?P<location>[^,]+), (?P<date>.+)$'
    title = soup.title.text
    #match = re.match(pattern,title)
    #csb.team_a_code = match.group('team_a_code')
    #csb.team_b_code = match.group('team_b_code')
    #csb.match = match.group('match')
    #csb.location = match.group('location')
    #csb.date = match.group('date')

def load_potm(soup, csb):
    csb.potm = soup.select_one('div.ds-w-1\\/3').contents[0].find('a').text
    #print(potm_div.text.strip())
    #divs = potm_div.find_all('div')
    #csb.potm = divs[0].text.trim()
    #print(potm_a.text)
    #for child in potm_div:
    #    if child.name:
    #        print(child.name)
    #        print(child.text.strip())

# def load_result(soup, csb):
#     result_div = soup.find('div', string='RESULT').find_next_sibling('div')
    
#     if  result_div:
#         results = result_div.text.strip().split(',')
#         csb.match = results[0]
#         csb.location = results[1]
#         csb.date = results[2] + ',' + results[3]
#         csb.series = results[4]

def load_match_details(soup, csb):
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
                    csb.umpire_1 = cells[1].text.strip().split('DRS')[0]
                    csb.umpire_2 = cells[1].text.strip().split('DRS')[1]
                
                if cells[0].text.strip() == 'Match Referee' :
                    csb.ref = cells[1].text.strip()

                if cells[0].text.strip() == 'Series' :
                    csb.series = cells[1].text.strip()

                if cells[0].text.strip() == 'Match days' :
                    csb.date = cells[1].text.split('-')[0].strip()

                if cells[0].text.strip() == 'Season' :
                    csb.season = cells[1].text.strip()




def scrape_espn(url):
    headers = {
        'User-Agent': bs.get_random_ua()
    }
    soup = get_soup2(url, headers)
    if soup:
        current_score_board = build_score_board(soup)
        
        
        load_title(soup, current_score_board)
        load_total_scores(soup, current_score_board)
        #load_scores(soup, current_score_board)
        load_potm(soup, current_score_board)
        load_match_details(soup, current_score_board)
        print(current_score_board)
