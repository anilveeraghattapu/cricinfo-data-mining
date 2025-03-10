import time
from code.crawler.url_crawler import *
import code.bot_settings.settings as bs
import random
years_list = []

def load_years():
    for y in range(1974,2026):
        years_list.append(y)
    years_list.remove(1977)


if __name__ == '__main__':
    load_years()
    #print(years_list)

    #for year in years_list:
    time.sleep(bs.SLEEP_INTERVAL)
    crawl_page(random.choice(years_list))