# -*- coding: utf-8 -*-
import os, time, re
import urlparse, random, getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


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
    time.sleep(random.uniform(3.4, 9.5))
    page_html = BeautifulSoup(browser.page_source)
    check_job_page(job_id, page_html)


def main():
    browser = webdriver.Firefox()
    browser.get('http://trampos.co/')

    home_page = BeautifulSoup(browser.page_source)
    #latest_job_id = get_latest_job_id(home_page)
    latest_job_id = '124714'

    latest_id_int = int(latest_job_id) + 1
    for job_id in reversed(range(latest_id_int)):
        get_job_opportunity(browser, job_id)


if __name__ == '__main__':
    main()
