#!/usr/bin/env python
# coding: utf-8

# 10.3.3
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# 10.5.3
def scrape_all():
    # 10.3.3
    #set up URL for scraping
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last _modified": dt.datetime.now()
    }

    # stop webdriver and return data
    browser.quit()
    return data

# 10.5.2
# define mars news function
def mars_news(browser):
    # 10.3.3
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
   
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # 10.3.3
    # set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #10.5.2
    # add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # 10.3.3
        # use parent element to find first 'a' tag and save as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # 10.3.3
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


# ### JPL Space Images Featured Image

# 10.5.2
# define featured image
def featured_image(browser):
    # 10.3.4
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # 10.3.4
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # 10.3.4
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # 10.5.2
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts
# 10.5.2
# define mars facts functions
def mars_facts():

    try:
        # 10.3.5
        # use 'read_html' to scrape the facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html(classes='table table-striped')

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())