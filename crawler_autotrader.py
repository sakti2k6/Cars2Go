import time
import random
from datetime import date
import json

from scrapper_autotrader import scrapper_autotrader

headers = ({'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
base_url = 'https://www.autotrader.com'

class crawler_autotrader:
    def run_spider(self):
        cnt = 0
        make_model = json.load(open('./files/Autotrader_Make_Model.json','r'))
        #locations = json.load(open('./files/Autotrader_Location.json','r'))
        # Only crawl for austin location and 2020 or newer cars
        for make, models in make_model.items():
            for model in models:
                url = f"{base_url}/cars-for-sale/{make}/{model}/austin-tx/?numRecords=100&startYear=2020"
                print(url)
                time.sleep(random.uniform(0.5,1.6))
                try:
                    scrapper_autotrader(url)
                    cnt += 1
                except Exception as e:
                    print(str(e))
        return cnt


if __name__ == "__main__":
    start_time = time.time()
    spider = crawler_autotrader()
    cnt = spider.run_spider()
    print(f"[INFO] AutoTrader all URLs {cnt} Crawled in {time.time()-start_time} seconds")
