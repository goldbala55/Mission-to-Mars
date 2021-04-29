#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Import Splinter and BeautifulSoup, Pandas
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[16]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[27]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[28]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[7]:


slide_elem


# In[11]:


slide_elem.find('div', class_='content_title')


# In[29]:


# Use the parent element to find the first `a` tag and save it as `news_title`
#
# - this works too :)
# news_title = slide_elem.find('div', class_='content_title').text
#
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[32]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[41]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[42]:


img_soup


# In[43]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[48]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
#img_url1 = f'{url}/{img_url_rel}'
img_url


# ### Mars Facts 

# In[57]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[58]:


df.to_html()


# In[14]:


browser.quit()


# In[63]:


df.to_html(classes="table table-striped")


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[17]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[18]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# make some soup
html = browser.html
mars_img_soup = soup(html, 'html.parser')

for i in range(4):
    hemi = browser.find_by_tag('h3')[i]
    hemi.click()
    # Parse the resulting html with soup
    html = browser.html
    hemi_img_soup = soup(html, 'html.parser')
    full_hemi_url = hemi_img_soup.find('div', class_ = 'downloads').find('a').get('href')
    full_hemi_title = hemi_img_soup.find_all('h2', class_ = 'title')[0].text
    img_dict={'img_url': full_hemi_url,
              'title': full_hemi_title
             }
    hemisphere_image_urls.append(img_dict)
    browser.back()


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[21]:


# 5. Quit the browser
browser.quit()


# In[ ]:




