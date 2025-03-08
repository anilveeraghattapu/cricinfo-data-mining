#import sys
import os
from code.scraper.scrape_url import scrape_espn
import code.bot_settings.settings as bs
import time
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':

    urls = bs.get_urls()
    for url in urls:
        time.sleep(bs.SLEEP_INTERVAL)
        scrape_espn(url)
        bs.logger.info(msg=f'scraping data from: {url}')