import requests
from bs4 import BeautifulSoup
import os
from time import sleep

url = 'https://www.gocomics.com/pearlsbeforeswine/2019/08/19'
count = 0
res=requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

while count < 10:
    res=requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    img = soup.find_all('img', {'class' : 'lazyload img-fluid'})

    img_url = img[1].get('src')
    img_res = requests.get(img_url)
    img_res.raise_for_status()

    img_file = open(os.path.basename(img_url), 'wb')
    for chunk in img_res.iter_content(100000):
        img_file.write(chunk)
    img_file.close()

    count += 1

    print('Downloading page ' + str(url))
    prev_url = int(url[-2:])-1
    url = "https://www.gocomics.com/pearlsbeforeswine/2019/08/" + str(prev_url)
