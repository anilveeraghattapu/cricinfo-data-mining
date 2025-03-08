import os
import requests

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

def get_tables(soup):
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        table_id = table.get('id', 'No ID')
        rows = table.find_all('tr')
        print(f"Table {i + 1} - ID: {table_id}, Rows: {len(rows)}")


def scrape_espn(url):
    headers = {
        'User-Agent': bs.get_random_ua()
    }
    soup = get_soup2(url, headers)
    if soup:
        current_score_board = build_score_board(soup)
        print(current_score_board.get_title())
        get_tables(soup)