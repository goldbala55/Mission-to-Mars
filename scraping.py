# Import Splinter, BeautifulSoup, Pandas and more
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # setup Splinter, initiate headless browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # get the news title and synopsis
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "mars_images": mars_hemisphere_images(browser),
        "last_modified": dt.datetime.now()
    }

    # Always close the automated browsing session when finished 
    browser.quit()

    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert the browser object to soup.
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #img_soup

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts
def mars_facts():

    try:
        # read in the html table and convert to pd
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # set the column names and add an index
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # return the df in html format, add bootstrap, use hover, remove stripe
    return  df.to_html(classes="table table-hover")

# ## Mars Hemisphere Images
def mars_hemisphere_images(browser):

    # Visit Hemisphere URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # list for images
    hemisphere_image_urls = []

    # retrieve the image urls and titles for each hemisphere.
    html = browser.html
    mars_img_soup = soup(html, 'html.parser')

    # There are 4 images to retrieve 
    for i in range(4):
        # find and 'click' each link to get full image
        try:
            hemi = browser.find_by_tag('h3')[i]
            hemi.click()
            # Parse the resulting html with soup
            html = browser.html
            hemi_img_soup = soup(html, 'html.parser')
            # find the downloads href and title, add them to the list 
            full_hemi_url = hemi_img_soup.find('div', class_ = 'downloads').find('a').get('href')
            full_hemi_title = hemi_img_soup.find_all('h2', class_ = 'title')[0].text
        except AttributeError:
            img_dict={'img_url': None, 'title': None}
            hemisphere_image_urls.append(img_dict)
        else:
            img_dict={'img_url': full_hemi_url,
                    'title': full_hemi_title
                    }
            hemisphere_image_urls.append(img_dict)
            browser.back()

    # return the list with image links and titles
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())