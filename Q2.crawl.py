from urllib import robotparser
import lxml.html
import time
import requests
from pqdict import pqdict

BASE_URL = 'https://en.wikipedia.org/wiki/Andy_Ram'
xpaths = ["//table[contains(@class,'sortable')]/tbody/tr/td[count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::th)+1]/a[1]/@href", "//table[contains(@class,'sortable')]/tbody/tr/td[count(../../tr/th[contains(text(),'Opponents')]/preceding-sibling::th)+1]/a[1]/@href", "//table[@class = 'infobox vcard']/tbody/tr/th[contains(text(),'Coach')]/../td//a/@href[contains(., 'wiki')]"]
WIKI = 'https://en.wikipedia.org'
MAX_NUM_OF_URLS_TO_CRAWLED = 100
TIME_TO_SLEEP = 3
'''
Purpose - crawl pages of tennis players in Wikipedia
url - to start crawling from
xpaths - accumulating the discovered URLs during crawling
'''


def crawl(url, xpaths):
    # crawling ethics
    rp = robotparser.RobotFileParser()
    rp.set_url(WIKI + "/robots.txt")
    rp.read()

    '''
    create db:
    1. results_urls- list of lists with [src url, evaluated url].
    2. urls that been crawled (by priority, relevant (wiki pages) and non-duplicated.
    3. seen urls - for not duplicate.
    '''
    source_url = url
    results_urls = []
    priority_urls_q = pqdict(reverse=True)  # get the most priority first
    seen_list = []
    priority_urls_q[source_url] = 1  # first time
    #  f = open('results.txt', 'w+')

    for i in range(MAX_NUM_OF_URLS_TO_CRAWLED):
        seen_list.append(source_url)  # add the url to seen list
        try:
            res = requests.get(source_url)
            doc = lxml.html.fromstring(res.content)
            for expath_expression in xpaths:
                for t in doc.xpath(expath_expression):
                    current_url = t
                    # if relative wikipedia address - make it absolute
                    current_url = WIKI + current_url if current_url.startswith('/wiki') else current_url
                    # if url isn't legal by Wikipedia or not an Wikipedia page - continue
                    if not rp.can_fetch("*", current_url) or not current_url.startswith(WIKI):
                        continue
                    # else - "good" url , add to results list and add to queue
                    urls_pair = [source_url, current_url]

                    # if cur url == src url or cur url has before from the src url - continue
                    if current_url == source_url or urls_pair in results_urls:
                        continue

                    # else - increase the priority
                    # if url seen not in first time - add 1 to priority queue
                    if current_url in list(priority_urls_q.keys()):
                        priority_urls_q[current_url] += 1
                    # first time
                    else:
                        priority_urls_q[current_url] = 1

                    # add to results list
                    if urls_pair not in results_urls:
                        #  f.write(str(urls_pair)+'\n')
                        results_urls.append(urls_pair)
        # error in crawling URL, dont insert to list and get another url
        except:
            continue

        # get the next url & make sure is is not in the seen list
        while True:
            source_url = priority_urls_q.pop()  # get the next url by the most times that it been seen
            if source_url not in seen_list:
                time.sleep(TIME_TO_SLEEP)
                break
            is_empty = len(priority_urls_q) == 0
            if is_empty:
                return results_urls

    #  f.close()
    return results_urls


# if __name__ == "__main__":
#     print(crawl(url=BASE_URL, xpaths=xpaths))
