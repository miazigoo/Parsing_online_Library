import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())

title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
print(title_text)
img_url = soup.find('img', class_='attachment-post-image')['src']
print(img_url)
text_soup = soup.find('div', class_='entry-content').find('p').text
print(text_soup)
