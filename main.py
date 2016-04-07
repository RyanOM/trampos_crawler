
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, re
import urlparse, random, getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

from idmarker import marker


def get_latest_job_id(homepagesoup):
    link_items = homepagesoup.find_all(class_='carousel')[0]
    job_url = link_items.contents[1].attrs['href']
    job_id = re.findall('[0-9]+', job_url)[0]
    return job_id


def check_job_page(job_id, page_html):

    if 'ENCONTRADA' in page_html.text:
        print '404: %s' % job_id
    elif 'pode ser visualizado por candidatos premium' in page_html.text:
        print 'premium: %s' % job_id
        oldest_premium = job_id
    elif 'VEJA OUTROS NA MESMA' in page_html.text:
        print 'Job no longer avaliable: %s' % job_id
    else:
        html = page_html.prettify("utf-8")
        file_name = "trampos-%s.html" % job_id
        file_path = 'job_offers/trampos/%s' % file_name
        if not os.path.isfile(file_path):
            with open(file_path, "wb") as htmlfile:
                htmlfile.write(html)
                print'Created file: %s' % file_name
        else:
            print'File already exists: %s' % file_name


def get_job_opportunity(browser, job_id):
    job_url = 'http://trampos.co/oportunidades/%s' % job_id
    browser.get(job_url)
    time.sleep(random.uniform(0.4, 2.5))
    page_html = BeautifulSoup(browser.page_source)
    check_job_page(job_id, page_html)


def main():
	display = Display(visible=0, size=(800, 600))
	#display.start()
	browser = webdriver.Firefox()
	browser.get('http://trampos.co/')
	home_page = BeautifulSoup(browser.page_source)
	latest_job_id = get_latest_job_id(home_page)
	#latest_job_id = '124714'
	# leave a marker to get on the next scrape
	oldest_premium = marker
	limit = marker

	latest_id_int = int(latest_job_id) + 1
	for job_id in reversed(range(latest_id_int)):
		terminate = os.path.isfile('./terminate.txt')
		if terminate or job_id < limit:
			with open('./idmarker.py', 'w') as marker_file:
				marker_file.write("marker = %s" %oldest_premium)
			browser.quit()
			if terminate:
				print("exiting due to terminate")
				os.remove('./terminate.txt')
			else:
				print("Finished scraping new docs")
			break
		else:
			get_job_opportunity(browser, job_id)


if __name__ == '__main__':
    main()
