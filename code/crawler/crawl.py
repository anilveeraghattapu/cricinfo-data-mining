import time
from code.crawler.url_crawler import *
import code.bot_settings.settings as bs
import random
years_list = []

# indian odis
def load_years():
    for y in range(1974,2026):
        years_list.append(y)
    years_list.remove(1977)

# years for all countries
def load_all_years():
    for y in range(1971,2026):
        years_list.append(y)

if __name__ == '__main__':
    load_all_years()

    for year in years_list:
        time.sleep(bs.SLEEP_INTERVAL)
        #crawl_page(year)
        print(f'{year} crawl completed!')