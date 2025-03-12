import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import code.bot_settings.settings as bs 
from urllib.parse import urljoin

#only indian odis
def get_url(year):
    return f'https://www.espncricinfo.com/records/year/team-match-results/{year}-{year}/one-day-internationals-2?team=6'

def get_all_countries_url(year):
    return f'https://www.espncricinfo.com/records/year/team-match-results/{year}-{year}/one-day-internationals-2'

def get_page(url):
    try:
        html = urlopen(url)
    except Exception as e:
        return None
    return BeautifulSoup(html, 'html.parser')


def get_page2(url=None, headers=None):
    with open(os.path.join(bs.cache_dir, 'page2.html'), 'r', encoding='utf-8') as file:
        html_content = file.read()
    return BeautifulSoup(html_content, 'html.parser')


def get_odi_urls(page):
    base_url = "https://www.espncricinfo.com"
    table = page.find('table')
    anchors = table.find_all('a')
    hrefs = []
    for tag in anchors:
        if 'ODI # ' in tag.text:
            relative_url = tag.get('href')
            full_url = urljoin(base_url, relative_url)
            hrefs.append(full_url)
    return hrefs

def write_urls(urls_list):
    #with open(bs.odis_file, 'a') as file:
    with open(bs.all_countries_odis_file, 'a') as file:
        for url in urls_list:
            file.write(url + '\n')
    bs.logger.info(msg=f'{len(urls_list)} URL(s) added to the list')


def crawl_page(year):
    url = get_all_countries_url(year)
    page = get_page(url)
    urls = get_odi_urls(page)
    write_urls(urls)
    