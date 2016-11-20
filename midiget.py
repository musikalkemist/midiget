# coding: utf-8
"""
(c) Valerio Velardo, velardovalerio@gmail.com, 2015

This program crawls the pages of a website and downloads all the midi files it
finds. The midi files are saved in a directory called 'savedmidi'. 
The program is launched from the command line. 2 parameters should be 
specified:
 1- the url of the start page 
 2- the max number of pages to crawl before the program stops

The second parameter is optional (default value = 1000 pages)
"""

import urllib
import re
import urlparse
import os
import errno
import sys
import bs4 as bs 
import time


def crawl_and_save(start_page, MAX_PAGES):
    """ Crawl pages of website from start_page and save all midi files"""
    
    start_time = time.time()
    page = 1
    links_to_crawl = [start_page]
    links_crawled = []
    url_files = []
    url_start_page = urlparse.urlparse(start_page)
    netloc = url_start_page.netloc    
    # loop over the pages of the website 
    while page <= MAX_PAGES:
        page_to_download = links_to_crawl[0]
        sauce = urllib.urlopen(page_to_download).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        # loop over all links in a page
        for link_tag in soup.find_all('a'):
            href = str(link_tag.get('href'))
            href = str(handle_relative_link(page_to_download, href))
            # check link wasn't encountered before and is internal
            if (href not in links_crawled and 
                href not in links_to_crawl and
                is_internal_link(href, netloc) and 
                href not in url_files):
                # check if links takes to a midi file
                if is_midi(href):
                    file_name = href.split('/')[-1]
                    url_files.append(href)
                    save_file(href, file_name)
                    print "Saved: ", file_name
                else:
                    links_to_crawl.append(href)
        links_crawled.append(links_to_crawl.pop(0))
        if page % 10 == True:
            pagesPerSec = (time.time() - start_time) / page
            print
            print 'Pages crawled:', page
            print 'Time so far:', time.time() - start_time, "sec" 
            print 'Avg time per page:', pagesPerSec, "sec"
            print
        page = page + 1
        # exit if MAX_pages is reached
        if page == MAX_PAGES:
            print
            print "Max no. of pages reached!"
            print
            sys.exit(0)
        # exit if all pages have been crawled
        if len(links_to_crawl) == 0:
            print
            print "All the pages of the website have been crawled!"
            print
            break
        
def is_internal_link(link, netloc):
    """ Check if a link belongs to the website"""
    
    return bool((re.search(netloc, link)))
    
# function needed to handle relative links
def save_file(url_file, file_name):  
    """ Save midi file in directory 'midisaves'"""
    
    path = "./savedmidi/" + file_name
    urllib.urlretrieve(url_file, path)

# handle relative links
def handle_relative_link(base_link, link):
    """" If necessary, transform relative links into absolute links"""
    
    if bool(re.search('^http', link)):
        return link
    else:        
        return urlparse.urljoin(base_link, link)

def is_midi(link):
    """ Check if a link leads to a midi file"""
    
    return bool(re.search('\.mid$|\.midi$', link))
    
def make_sure_path_exists(path):
    """ Check if 'savemidi' directory exists, otherwise create it"""
    
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def check_type_max_pages(MAX_PAGES):
    """ Check that max_pages argument input by user is int"""
    
    try:
        int(MAX_PAGES)
    except ValueError:
        print
        print "The 2nd argument (i.e., max no. pages) must be an integer."
        print
        sys.exit(0)

def check_no_args(arguments):
    """ Check that user has input at least 1 argument"""
    
    if len(arguments) < 2:
        print
        print "At least 1 argument (i.e., start page) must be provided."
        print
        sys.exit(0)
        
def check_start_page_url(start_page):
    """ Check that start_page argument input by the user is a valid url"""
    
    try:
        urllib.urlopen(start_page).read()
    except IOError:
        print
        print "Insert valid url (e.g., http://google.com)."
        print
        sys.exit(0)
        
if __name__ == "__main__":
    # check args are ok
    check_no_args(sys.argv)
    start_page = sys.argv[1]
    check_start_page_url(start_page)
    if len(sys.argv) > 2:
        check_type_max_pages(sys.argv[2])
        MAX_PAGES = int(sys.argv[2])
    else:
        MAX_PAGES = 1000
    make_sure_path_exists("./savedmidi")
    crawl_and_save(start_page, MAX_PAGES)    
    










