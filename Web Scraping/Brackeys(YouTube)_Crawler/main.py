from bs4 import BeautifulSoup
import pandas as pd

# open saved html
with open('full_html.html' ,'r',encoding='utf-8') as html_file:
    html = html_file.read()


soup = BeautifulSoup(html , 'lxml')


videos = soup.find_all('ytd-grid-video-renderer' , class_ = 'style-scope ytd-grid-renderer') # get all videos

name_c,view_c,time_c,link_c = [],[],[],[] # set lists for dataframe

for video in videos:
    name = video.find('a', class_ = 'yt-simple-endpoint style-scope ytd-grid-video-renderer' )['title']

    view , time = video.find_all('span' , class_ = 'style-scope ytd-grid-video-renderer')

    link = video.find('a' , class_ = 'yt-simple-endpoint inline-block style-scope ytd-thumbnail')['href']

    name_c.append(name)
    view_c.append(view.text)
    time_c.append(time.text)
    link_c.append(f'https://www.youtube.com{link}')



data = pd.DataFrame({'video name':name_c , 'views':view_c , 'time' : time_c , 'link':link_c}) # create dataframe

data.to_excel('result.xlsx', index=False  )


