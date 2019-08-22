import requests
from bs4 import BeautifulSoup
import os
from time import sleep

url = 'https://www.gocomics.com/pearlsbeforeswine/'
count = 0
res=requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

# find current link
soup2 = soup.select('div .row')
links = soup2[0].find_all('a', class_='gc-blended-link gc-blended-link--primary')
link = 'http://www.gocomics.com' + links[0].get('href')

while count < 10:
    res=requests.get(link)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # find image link
    img = soup.find_all('img', {'class' : 'lazyload img-fluid'})
    img_url = img[1].get('src')
    img_res = requests.get(img_url)
    img_res.raise_for_status()

    # download images
    img_file = open(os.path.basename(img_url), 'wb')
    for chunk in img_res.iter_content(100000):
        img_file.write(chunk)
    img_file.close()

    print('Downloading page ' + str(count + 1) + ' ' + str(link))

    count += 1

    # find previous link

    container = soup.select('div .gc-calendar-nav__previous')[0].select('a')
    prev_link = container[1].get('href')
    link = 'http://www.gocomics.com' + prev_link
